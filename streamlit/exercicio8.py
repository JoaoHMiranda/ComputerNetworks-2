import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def main():
    st.title("Aplicativo de Previsão com Machine Learning")
    
    st.write("Este aplicativo utiliza um modelo de regressão linear para prever a nota final com base em horas de estudo e nota anterior.")
    
    # Gerando dados fictícios para treinamento
    np.random.seed(42)
    horas_estudo = np.random.uniform(0, 10, 100)  # horas de estudo entre 0 e 10
    nota_anterior = np.random.uniform(5, 10, 100)  # nota anterior entre 5 e 10
    # Relação: nota_final = 0.5 * nota_anterior + 0.3 * horas_estudo + ruído
    ruido = np.random.normal(0, 0.5, 100)
    nota_final = 0.5 * nota_anterior + 0.3 * horas_estudo + ruido

    # Criando DataFrame com os dados
    df = pd.DataFrame({
        "horas_estudo": horas_estudo,
        "nota_anterior": nota_anterior,
        "nota_final": nota_final
    })
    
    if st.checkbox("Mostrar dados de treinamento"):
        st.write(df)
    
    # Treinamento do modelo de regressão linear
    X = df[["horas_estudo", "nota_anterior"]]
    y = df["nota_final"]
    model = LinearRegression()
    model.fit(X, y)
    
    st.subheader("Insira os valores para previsão:")
    
    # Entrada dos dados pelo usuário
    horas_input = st.number_input("Horas de estudo:", min_value=0.0, max_value=24.0, value=5.0, step=0.1)
    nota_anterior_input = st.number_input("Nota anterior:", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
    
    # Previsão do modelo
    entrada = np.array([[horas_input, nota_anterior_input]])
    previsao = model.predict(entrada)
    
    # Limita a nota final prevista a 10, se necessário
    nota_final_prevista = previsao[0]
    if nota_final_prevista > 10:
        nota_final_prevista = 10
    
    st.write(f"Nota final prevista: {nota_final_prevista:.2f}")
    
    st.subheader("Comparação entre Dados de Entrada e Previsão:")
    # Criação de DataFrame para o gráfico de barras
    dados_grafico = {
        "Variáveis": ["Horas de Estudo", "Nota Anterior", "Nota Final Prevista"],
        "Valores": [horas_input, nota_anterior_input, nota_final_prevista]
    }
    df_grafico = pd.DataFrame(dados_grafico)
    df_grafico = df_grafico.set_index("Variáveis")
    
    st.bar_chart(df_grafico)

if __name__ == '__main__':
    main()
