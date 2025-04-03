# server.py
# Joao Henrique Silva
import socket
import json

# Config do servidor
HOST = 'localhost'
PORTA = 9999

# criando socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORTA))
print(f"Servidor iniciado em {HOST}:{PORTA}")

# intervalos para cálculo de números primos
inicio_total = 1
fim_total = 100000000# 100 milhoes
subintervalo = 10000# 10 mil


# lista de tarefas 
tarefas = [(inicio, min(inicio + subintervalo - 1, fim_total))
           for inicio in range(inicio_total, fim_total + 1, subintervalo)]
total_tarefas = len(tarefas)
print(f"Total de tarefas: {total_tarefas}")

tarefas_atribuidas = 0 
tarefas_concluidas = 0 
primos_encontrados = set()  # armazenar os números primos encontrados

client_conect=set()
exit=True
# loop do servidor
while exit:
    try:
        # recebendo dados do cliente
        dados, endereco_cliente = servidor.recvfrom(65535)
        mensagem = json.loads(dados.decode('utf-8'))
        if endereco_cliente not in client_conect:
            client_conect.add(endereco_cliente)
        
        # ver tipo de mensagem do cliente 

        #qunado é request
        if mensagem.get("type") == "request":

            # caso as tarefas ja tenham sido comcluidas
            # finaliza o cliente
            if tarefas_atribuidas >= total_tarefas:
                client_conect.remove(endereco_cliente)
                if len(client_conect) == 0:
                    exit=False
                mensagem_fim = json.dumps({"type": "done"})
                servidor.sendto(mensagem_fim.encode('utf-8'), endereco_cliente)
                print(f"Enviada mensagem 'done' para {endereco_cliente}")
                continue

            # caso ainda tenha tarefa sobrando
            tarefa = tarefas.pop(0)
            tarefas_atribuidas += 1
            mensagem_tarefa = json.dumps({
                "type": "task",
                "range": [tarefa[0], tarefa[1]]
            })
            servidor.sendto(mensagem_tarefa.encode('utf-8'), endereco_cliente)
            print(f"Tarefa {tarefa} enviada para {endereco_cliente}")
        
        # quando e resultado
        elif mensagem.get("type") == "result":
            primos = mensagem.get("primes", [])
            print(f"Recebido resultado com {len(primos)} primos de {endereco_cliente}")
            primos_encontrados.update(primos)
            tarefas_concluidas += 1
  
    # erro
    except Exception as erro:
        print("Erro no servidor:", erro)

# apos processar todas as tarefas

print("Todas as tarefas foram concluidas.")
print(f"Total de números primos encontrados: {len(primos_encontrados)}")
with open("primes.txt", "w") as arquivo:
    for primo in sorted(primos_encontrados):
        arquivo.write(str(primo) + "\n")
print("Resultados salvos em primos.txt")
servidor.close()