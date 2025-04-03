import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("Dashboard de Análise de Dados")
    st.write("Faça o upload do seu arquivo CSV para análise.")

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Leitura do CSV com Pandas
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Prévia dos Dados")
        st.dataframe(df)

        # Identifica colunas numéricas inicialmente
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        # Se não houver colunas numéricas, tenta converter todas as colunas para numéricas
        if not numeric_columns:
            st.info("Nenhuma coluna numérica encontrada. Tentando converter colunas para numéricas.")
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        # Remove as colunas que possuem somente NaN
        numeric_columns = [col for col in numeric_columns if not df[col].isna().all()]

        if numeric_columns:
            st.subheader("Análise Estatística")
            # Permite ao usuário selecionar uma coluna numérica
            selected_column = st.selectbox("Selecione uma coluna numérica para análise:", numeric_columns)
            
            # Cálculos estatísticos
            mean_val = df[selected_column].mean()
            median_val = df[selected_column].median()
            std_val = df[selected_column].std()

            st.write(f"**Média de {selected_column}:** {mean_val:.2f}")
            st.write(f"**Mediana de {selected_column}:** {median_val:.2f}")
            st.write(f"**Desvio Padrão de {selected_column}:** {std_val:.2f}")

            # Criação do histograma com Plotly
            st.subheader("Histograma")
            fig = px.histogram(df, x=selected_column, title=f"Distribuição de {selected_column}")
            st.plotly_chart(fig)
        else:
            st.warning("O arquivo CSV não contém colunas numéricas válidas para análise.")

if __name__ == '__main__':
    main()
