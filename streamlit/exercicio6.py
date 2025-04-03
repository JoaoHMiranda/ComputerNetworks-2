import streamlit as st
from wordcloud import WordCloud
from collections import Counter

def main():
    st.title("Análise de Texto com Processamento em Tempo Real")
    st.write("Insira um texto longo para ver a contagem de palavras, caracteres, uma nuvem de palavras e as 5 palavras mais frequentes.")

    # Área de texto para o usuário inserir o texto
    text = st.text_area("Digite o seu texto aqui:", height=200)

    # Widget para o usuário escolher o número mínimo de caracteres
    min_length = st.slider("Escolha o número mínimo de caracteres para considerar nas análises:", min_value=1, max_value=10, value=4, step=1)
    
    if text:
        # Divisão do texto em palavras e contagem básica
        words = text.split()
        num_words = len(words)
        num_chars = len(text)
        
        st.subheader("Estatísticas do Texto")
        st.write(f"**Número de palavras:** {num_words}")
        st.write(f"**Número de caracteres:** {num_chars}")

        # Função auxiliar para limpar a palavra (remover pontuação e converter para minúsculas)
        def clean_word(word):
            return word.strip(".,!?;:\"()[]").lower()

        # Filtra as palavras considerando o tamanho mínimo escolhido
        filtered_words = [clean_word(word) for word in words if len(clean_word(word)) >= min_length]
        filtered_text = " ".join(filtered_words)
        
        # Gera a nuvem de palavras com as palavras filtradas
        if filtered_text:
            wc = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)
            wc_image = wc.to_array()
            st.subheader("Nuvem de Palavras")
            st.image(wc_image)
        else:
            st.warning("Nenhuma palavra com o tamanho mínimo especificado foi encontrada para a nuvem de palavras.")
        
        # Identifica as 5 palavras mais frequentes entre as palavras filtradas
        word_counts = Counter(filtered_words)
        top_5 = word_counts.most_common(5)
        
        st.subheader(f"5 Palavras Mais Frequentes (mínimo {min_length} caracteres)")
        if top_5:
            for word, count in top_5:
                st.write(f"{word}: {count}")
        else:
            st.warning("Nenhuma palavra com o tamanho mínimo especificado foi encontrada.")

if __name__ == "__main__":
    main()
