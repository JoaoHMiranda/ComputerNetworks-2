import socket
import threading
import hashlib
import os

# Lista global de conexões de clientes
clients = []

def compute_file_hash(data: bytes) -> str:
    """
    Calcula o hash SHA-256 de 'data' (bytes).
    Retorna a string hexadecimal resultante.
    """
    return hashlib.sha256(data).hexdigest()

def broadcast_update(sender_conn, filename, data, file_hash):
    """
    Envia para todos os clientes (exceto o que enviou o UPDATE)
    uma notificação de que o arquivo foi atualizado, incluindo o novo conteúdo.

    Formato:
      UPDATE <filename> <size> <hash>\n
      <conteúdo em bytes>
    """
    for c in clients:
        if c != sender_conn:
            try:
                c.sendall(f"UPDATE {filename} {len(data)} {file_hash}\n".encode('utf-8'))
                c.sendall(data)
            except:
                pass  # Pode tratar erros de envio, se desejar

def handle_client(conn, addr):
    """
    Executado em uma thread separada para cada cliente.
    Lê comandos do cliente e responde de acordo (REQUEST, UPDATE etc.).
    """
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                # Se veio vazio, o cliente encerrou
                break
            
            parts = msg.split()
            cmd = parts[0].upper()

            if cmd == "REQUEST":
                # REQUEST <filename>
                filename = parts[1]

                # Se o arquivo não existe, responde NOT_FOUND
                if not os.path.exists(filename):
                    conn.sendall("NOT_FOUND\n".encode('utf-8'))
                else:
                    # Se existe, envia FILE <filename> <size> <hash>\n + dados
                    with open(filename, 'rb') as f:
                        data = f.read()
                    file_hash = compute_file_hash(data)
                    conn.sendall(f"FILE {filename} {len(data)} {file_hash}\n".encode('utf-8'))
                    conn.sendall(data)

            elif cmd == "UPDATE":
                # UPDATE <filename> <tamanho> <hash>
                filename = parts[1]
                length = int(parts[2])
                new_hash = parts[3]

                # Recebe o conteúdo (em 'length' bytes)
                file_data = b""
                remaining = length
                while remaining > 0:
                    chunk = conn.recv(min(4096, remaining))
                    if not chunk:
                        break
                    file_data += chunk
                    remaining -= len(chunk)
                
                # Cria ou sobrescreve o arquivo
                with open(filename, 'wb') as f:
                    f.write(file_data)

                print(f"[UPDATE] {addr} atualizou ou criou '{filename}' (hash={new_hash}).")
                
                # Notifica os outros clientes
                broadcast_update(conn, filename, file_data, new_hash)

                # Envia confirmação ao próprio cliente que fez o UPDATE
                conn.sendall("UPDATE_OK\n".encode('utf-8'))

            else:
                conn.sendall("UNKNOWN_COMMAND\n".encode('utf-8'))

        except ConnectionResetError:
            # Cliente caiu abruptamente
            break

    conn.close()
    if conn in clients:
        clients.remove(conn)
    print(f"[DESCONEXÃO] {addr} desconectado.")

def check_exit():
    """
    Thread auxiliar que, no console do servidor, permite digitar "EXIT"
    para encerrar o servidor.
    """
    while True:
        command = input("")
        # Agora, só encerrar se for "EXIT" em maiúsculo:
        if command == "EXIT":
            print("[Encerrando] Servidor encerrado via console.")
            os._exit(0)

def start_server(host='localhost', port=5000):
    """
    Função principal do servidor:
    - Cria socket
    - Faz bind
    - Faz listen
    - Cria thread para 'EXIT'
    - Fica aceitando conexões e iniciando threads handle_client
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[INICIADO] Servidor ouvindo em {host}:{port}")
    print("Digite 'EXIT' aqui para encerrar o servidor.")

    exit_thread = threading.Thread(target=check_exit, daemon=True)
    exit_thread.start()

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
