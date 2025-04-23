# Monitoramento de Tráfego de Rede

**O que é?**  
Uma aplicação web para simular o monitoramento de dispositivos de rede.  
Permite registrar IP, nome e taxa de tráfego (Mbps), visualizar status (Normal < 50 Mbps / Alto ≥ 50 Mbps) com cores, exibir gráfico de barras colorido e remover dispositivos.

## Como rodar com Docker

1. Clone o repositório e acesse a pasta:
   ```bash
   git clone <URL_DO_REPO>
   cd network_monitor_app

2. Construa a imagem Docker:
    ```bash
    docker build -t network-monitor-app .

3. Execute o container em background:
    ```bash
    docker run -d --name monitor-app -p 5000:5000 -p 8501:8501 network-monitor-app

4. Abra no navegador:
    http://localhost:8501