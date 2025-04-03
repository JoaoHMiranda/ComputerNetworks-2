import streamlit as st
import pandas as pd
import numpy as np

def main():
    # Gerando dados de exemplo
    np.random.seed(42)
    data = {
        "Cidade": np.random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte"], size=100),
        "Categoria": np.random.choice(["A", "B", "C"], size=100),
        "Valor": np.random.randint(1, 100, size=100)
    }
    df = pd.DataFrame(data)

    st.title("Filtro Dinâmico em Tabela")
    st.write("Exemplo de aplicação com filtros interativos para dados.")

    # Filtros interativos para colunas categóricas
    selected_cidades = st.multiselect("Selecione Cidade(s):", options=df["Cidade"].unique(), default=df["Cidade"].unique())
    selected_categorias = st.multiselect("Selecione Categoria(s):", options=df["Categoria"].unique(), default=df["Categoria"].unique())

    # Filtro interativo para coluna numérica 'Valor'
    min_valor = int(df["Valor"].min())
    max_valor = int(df["Valor"].max())
    valor_range = st.slider("Selecione a faixa de Valor:", min_value=min_valor, max_value=max_valor, value=(min_valor, max_valor))

    # Aplicando os filtros ao DataFrame
    filtered_df = df[
        (df["Cidade"].isin(selected_cidades)) &
        (df["Categoria"].isin(selected_categorias)) &
        (df["Valor"] >= valor_range[0]) &
        (df["Valor"] <= valor_range[1])
    ]

    st.subheader("Tabela Filtrada")
    st.dataframe(filtered_df)


if __name__ == '__main__':
    main()