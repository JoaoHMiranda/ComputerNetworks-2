import streamlit as st
import pandas as pd

def main():
    st.title("Mapa Interativo com Dados Geográficos")
    st.write("Exiba pontos geográficos em um mapa interativo e filtre por categoria.")

    # Gerando um conjunto de dados de exemplo
    data = {
        "Categoria": ["Cidade", "Evento", "Cidade", "Evento", "Cidade", "Evento"],
        "Latitude": [-23.550520, -22.906847, -19.917, -15.794229, -25.4284, -21.780],
        "Longitude": [-46.633308, -43.172896, -43.9345, -47.882166, -49.2733, -43.000]
    }
    df = pd.DataFrame(data)

    st.subheader("Dados Geográficos")
    st.dataframe(df)

    # Filtro interativo para selecionar uma categoria específica
    categorias = df["Categoria"].unique().tolist()
    selected_category = st.selectbox("Selecione uma categoria:", options=categorias)

    # Filtrar os dados de acordo com a categoria selecionada
    filtered_df = df[df["Categoria"] == selected_category]

    # Renomear as colunas para que o st.map as reconheça
    filtered_df = filtered_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

    st.subheader("Mapa Interativo")
    st.map(filtered_df)

if __name__ == '__main__':
    main()
