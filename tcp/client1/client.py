import socket
import threading
import hashlib
import sys
import os

def compute_file_hash(data: bytes) -> str:
    """
    Calcula o hash SHA-256 de 'data'.
    """
    return hashlib.sha256(data).hexdigest()

def listen_server(sock: socket.socket):
    """
    Thread que escuta mensagens do servidor:
     - FILE <filename> <size> <hash>
     - NOT_FOUND
     - UPDATE <filename> <size> <hash>
     - UPDATE_OK
     - UNKNOWN_COMMAND
    """
    while True:
        try:
            header_data = sock.recv(1024)
            if not header_data:
                print("Conexão com o servidor foi encerrada.")
                break
            
            # Divide até a primeira quebra de linha
            parts = header_data.split(b'\n', 1)
            header = parts[0].decode('utf-8').split()
            cmd = header[0].upper()

            if cmd == "FILE":
                # FILE <filename> <size> <hash>
                filename = header[1]
                length = int(header[2])
                file_hash = header[3]

                file_data = b""
                if len(parts) > 1:
                    file_data = parts[1]

                # Completa a leitura do arquivo se ainda faltar
                while len(file_data) < length:
                    chunk = sock.recv(length - len(file_data))
                    if not chunk:
                        break
                    file_data += chunk

                # Salva localmente com o mesmo nome
                with open(filename, 'wb') as f:
                    f.write(file_data)

                print(f"[RECEBIDO] Arquivo '{filename}' (tamanho={length}, hash={file_hash}) salvo localmente.")
                print("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ", end="", flush=True)

            elif cmd == "NOT_FOUND":
                print("[ERRO] O arquivo requisitado não existe no servidor.")
                print("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ", end="", flush=True)

            elif cmd == "UPDATE":
                # UPDATE <filename> <size> <hash>
                filename = header[1]
                length = int(header[2])
                file_hash = header[3]

                file_data = b""
                if len(parts) > 1:
                    file_data = parts[1]

                while len(file_data) < length:
                    chunk = sock.recv(length - len(file_data))
                    if not chunk:
                        break
                    file_data += chunk

                # Salva/atualiza localmente
                with open(filename, 'wb') as f:
                    f.write(file_data)

                print(f"[UPDATE] Recebida nova versão de '{filename}' (hash={file_hash}).")
                print("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ", end="", flush=True)

            elif cmd == "UPDATE_OK":
                print("[CONFIRMAÇÃO] Arquivo atualizado/criado com sucesso no servidor.")
                print("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ", end="", flush=True)

            elif cmd == "UNKNOWN_COMMAND":
                print("[ERRO] Comando desconhecido no servidor.")
                print("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ", end="", flush=True)

            else:
                # Caso de resposta inesperada
                print("[AVISO] Resposta desconhecida do servidor:", header_data.decode('utf-8'))
                print("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ", end="", flush=True)

        except ConnectionResetError:
            print("Conexão foi finalizada pelo servidor.")
            break
        except Exception as e:
            print(f"[ERRO] Problema ao receber dados: {e}")
            break

    sock.close()

def main():
    if len(sys.argv) < 3:
        print(f"Uso: python {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    # Conecta ao servidor
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"[CONECTADO] Cliente conectado ao servidor em {host}:{port}")
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor.")
        sys.exit(1)

    # Thread para ouvir as mensagens do servidor
    t = threading.Thread(target=listen_server, args=(sock,))
    t.daemon = True
    t.start()

    # Loop de interação com o usuário
    while True:
        cmd = input("> Comando (REQUEST <arq>, UPDATE <arq> ou EXIT): ").strip()
        if not cmd:
            print("[ERRO] Você não digitou nada.")
            continue

        parts = cmd.split()
        action = parts[0].upper()

        if sock.fileno() == -1:
            print("[ERRO] Socket fechado. Encerrando cliente.")
            break

        if action == "REQUEST":
            # REQUEST <filename>
            if len(parts) < 2:
                print("[ERRO] Uso correto: REQUEST <filename>")
                continue
            filename = parts[1]
            sock.sendall(f"REQUEST {filename}".encode('utf-8'))

        elif action == "UPDATE":
            # UPDATE <filename>
            if len(parts) < 2:
                print("[ERRO] Uso correto: UPDATE <filename>")
                continue
            filename = parts[1]
            if not os.path.exists(filename):
                print(f"[ERRO] Arquivo '{filename}' não existe localmente para enviar.")
                continue

            with open(filename, 'rb') as f:
                data = f.read()

            file_hash = compute_file_hash(data)
            length = len(data)

            # Envia o comando e depois o conteúdo
            sock.sendall(f"UPDATE {filename} {length} {file_hash}\n".encode('utf-8'))
            sock.sendall(data)

        elif action == "EXIT":
            print("[Encerrando] Conexão com o servidor...")
            sock.close()
            break

        else:
            print("[ERRO] Comando inválido! Use: REQUEST <arq>, UPDATE <arq> ou EXIT.")

if __name__ == "__main__":
    main()
