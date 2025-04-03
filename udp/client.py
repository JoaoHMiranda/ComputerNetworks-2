# client.py
# Joao Henrique Silva
import socket
import json
import math

def crivo_eratostenes(inicio, fim):
    # retorna uma lista booleana de tamanho (fim - inicio + 1)

    tamanho = fim - inicio + 1
    is_prime = [True] * tamanho

    # se o intervalo inclui 0 ou 1, marque-os como não primos.
    if inicio == 0:
        is_prime[0] = False
        if fim >= 1:
            is_prime[1 - inicio] = False
    elif inicio == 1:
        is_prime[0] = False

    # obter todos os primos até a raiz quadrada de fim
    limite = int(math.sqrt(fim)) + 1
    is_prime_pequeno = [True] * (limite + 1)
    is_prime_pequeno[0] = is_prime_pequeno[1] = False
    for i in range(2, limite + 1):
        if is_prime_pequeno[i]:
            for j in range(i * i, limite + 1, i):
                is_prime_pequeno[j] = False
    primos_pequenos = [p for p, primo in enumerate(is_prime_pequeno) if primo]

    # marcar os múltiplos dos primos encontrados no intervalo [inicio, fim]
    for p in primos_pequenos:
        # o primeiro múltiplo de p no intervalo pode ser max(p*p, ceil(inicio/p)*p)
        start = max(p * p, ((inicio + p - 1) // p) * p)
        for j in range(start, fim + 1, p):
            is_prime[j - inicio] = False

    return is_prime

def obter_primos_intervalo(inicio, fim):
    # retorna uma lista dos números primos no intervalo [inicio, fim]
    
    crivo = crivo_eratostenes(inicio, fim)
    return [num for num, primo in enumerate(crivo, start=inicio) if primo]

# configuração do cliente
SERVIDOR = 'localhost'
PORTA = 9999
endereco_servidor = (SERVIDOR, PORTA)

# criando o socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Cliente iniciado. Conectando ao servidor {SERVIDOR}:{PORTA}")

while True:
    try:
        # enviar solicitação de tarefa ao servidor
        mensagem_solicitacao = json.dumps({"type": "request"})
        cliente.sendto(mensagem_solicitacao.encode('utf-8'), endereco_servidor)

        # receber resposta do servidor
        dados, _ = cliente.recvfrom(65535)
        mensagem = json.loads(dados.decode('utf-8'))

        # verificar tipo de mensagem do servidor
        # se for task

        if mensagem.get("type") == "task":
            inicio, fim = mensagem.get("range")
            print(f"Tarefa recebida: encontrar primos entre {inicio} e {fim}")
            primos = obter_primos_intervalo(inicio, fim)
            mensagem_resultado = json.dumps({
                "type": "result",
                "primes": primos
            })
            cliente.sendto(mensagem_resultado.encode('utf-8'), endereco_servidor)
            print(f"Resultado enviado com {len(primos)} primos encontrados.")
            
        # se for done
        elif mensagem.get("type") == "done":
            print("Nao ha mais tarefas. Finalizando cliente.")
            exit(0)

    except Exception as erro:
        print("Erro no cliente:", erro)
        break

cliente.close()
