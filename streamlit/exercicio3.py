import streamlit as st
import pandas as pd

def main():
    st.title("Simulador de Investimento")
    st.write("Simule o crescimento do seu investimento com juros compostos.")

    # Entrada do Valor Inicial
    valor_inicial = st.number_input("Valor Inicial (R$):", min_value=0.0, value=1000.0, step=100.0)

    # Entrada da Taxa de Juros Anual (em %)
    taxa_juros = st.slider("Taxa de Juros Anual (%):", min_value=0.0, max_value=20.0, value=5.0, step=0.1)

    # Entrada do Período em anos via selectbox (Exemplo: de 1 a 30 anos)
    periodos = list(range(1, 31))
    periodo_anos = st.selectbox("Período (anos):", options=periodos)

    # Conversão da taxa de juros para decimal
    taxa_decimal = taxa_juros / 100

    # Criação de DataFrame para armazenar os valores ao longo do tempo (inclui ano 0)
    anos = list(range(periodo_anos + 1))
    valores = [valor_inicial * (1 + taxa_decimal) ** ano for ano in anos]

    df_simulacao = pd.DataFrame({
        "Ano": anos,
        "Valor": valores
    })

    # Exibe o montante final
    montante_final = valores[-1]
    st.subheader("Resultado da Simulação")
    st.write(f"Após {periodo_anos} anos, o montante final será de: R$ {montante_final:,.2f}")

    # Exibe o gráfico de linha mostrando o crescimento
    st.subheader("Crescimento do Investimento ao Longo do Tempo")
    st.line_chart(df_simulacao.set_index("Ano"))

if __name__ == '__main__':
    main()
