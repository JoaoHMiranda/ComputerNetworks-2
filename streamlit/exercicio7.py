import streamlit as st
import pandas as pd

def main():
    st.title("Sistema de Recomendação Simples")
    
    st.header("Escolha seus gêneros favoritos:")
    
    # Cria checkboxes para os gêneros
    acao = st.checkbox("Ação")
    comedia = st.checkbox("Comédia")
    drama = st.checkbox("Drama")
    ficcao = st.checkbox("Ficção Científica")
    
    # Lista para armazenar os gêneros selecionados
    selected_genres = []
    if acao:
        selected_genres.append("Ação")
    if comedia:
        selected_genres.append("Comédia")
    if drama:
        selected_genres.append("Drama")
    if ficcao:
        selected_genres.append("Ficção Científica")
    
    # Dicionário com recomendações para cada gênero (título e pontuação)
    recommendations = {
        "Ação": [
            {"Título": "Mad Max: Estrada da Fúria", "Pontuação": 9},
            {"Título": "John Wick", "Pontuação": 8}
        ],
        "Comédia": [
            {"Título": "Se Beber, Não Case!", "Pontuação": 7},
            {"Título": "A Noite é Delas", "Pontuação": 8}
        ],
        "Drama": [
            {"Título": "Forrest Gump", "Pontuação": 9},
            {"Título": "O Poderoso Chefão", "Pontuação": 10}
        ],
        "Ficção Científica": [
            {"Título": "Blade Runner 2049", "Pontuação": 8},
            {"Título": "Interstellar", "Pontuação": 9}
        ]
    }
    
    # Agrega as recomendações com base nos gêneros selecionados
    all_recommendations = []
    for genre in selected_genres:
        all_recommendations.extend(recommendations.get(genre, []))
    
    if all_recommendations:
        st.subheader("Recomendações:")
        # Exibe a lista de recomendações
        for rec in all_recommendations:
            st.write(f"{rec['Título']} - Pontuação: {rec['Pontuação']}")
        
        # Cria um DataFrame para o gráfico de barras
        df = pd.DataFrame(all_recommendations)
        df_chart = df.set_index("Título")
        
        st.subheader("Pontuação das Recomendações:")
        st.bar_chart(df_chart)
    else:
        st.write("Selecione pelo menos um gênero para ver as recomendações!")

if __name__ == '__main__':
    main()
