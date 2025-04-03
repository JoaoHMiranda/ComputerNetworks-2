import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Selecione a Página:", 
                            ["Upload e Visualização de Dados", 
                             "Análise Estatística", 
                             "Gráficos Interativos"])
    
    # Inicializa o armazenamento dos dados no session_state
    if 'data' not in st.session_state:
        st.session_state.data = None

    if page == "Upload e Visualização de Dados":
        upload_data()
    elif page == "Análise Estatística":
        analyze_data()
    elif page == "Gráficos Interativos":
        interactive_charts()

def upload_data():
    st.title("Página 1: Upload e Visualização de Dados")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        # Lê o arquivo CSV e armazena no session_state
        data = pd.read_csv(uploaded_file)
        st.session_state.data = data
        st.write("Prévia dos Dados:")
        st.dataframe(data)
    else:
        st.write("Faça o upload de um arquivo CSV para visualizar os dados.")

def analyze_data():
    st.title("Página 2: Análise Estatística")
    if st.session_state.data is not None:
        df = st.session_state.data.copy()  # Trabalha com uma cópia para não modificar os dados originais
        st.subheader("Prévia dos Dados")
        st.dataframe(df)
        
        # Identifica colunas numéricas
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_columns:
            # Tenta converter as colunas para numéricas sem exibir alerta
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        # Remove colunas que possuem somente valores NaN
        numeric_columns = [col for col in numeric_columns if not df[col].isna().all()]
        
        if numeric_columns:
            st.subheader("Estatísticas de Colunas Numéricas")
            selected_column = st.selectbox("Selecione uma coluna numérica para análise:", numeric_columns)
            
            # Cálculo de estatísticas
            mean_val = df[selected_column].mean()
            median_val = df[selected_column].median()
            std_val = df[selected_column].std()

            st.write(f"**Média de {selected_column}:** {mean_val:.2f}")
            st.write(f"**Mediana de {selected_column}:** {median_val:.2f}")
            st.write(f"**Desvio Padrão de {selected_column}:** {std_val:.2f}")
        else:
            st.warning("O arquivo CSV não contém colunas numéricas válidas para análise.")
    else:
        st.write("Nenhum dado disponível. Por favor, faça o upload na Página 1.")

def interactive_charts():
    st.title("Página 3: Gráficos Interativos")
    if st.session_state.data is not None:
        df = st.session_state.data.copy()
        st.write("Selecione uma coluna numérica para gerar um gráfico interativo:")
        
        # Identifica colunas numéricas sem exibir alerta
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_columns:
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        numeric_columns = [col for col in numeric_columns if not df[col].isna().all()]
        
        if numeric_columns:
            selected_column = st.selectbox("Selecione uma coluna numérica:", numeric_columns)
            st.subheader(f"Gráfico interativo da coluna: {selected_column}")
            # Cria o histograma com Plotly
            fig = px.histogram(df, x=selected_column, title=f"Distribuição de {selected_column}", nbins=30)
            st.plotly_chart(fig)
        else:
            st.warning("O arquivo CSV não contém colunas numéricas válidas para gráficos interativos.")
    else:
        st.write("Nenhum dado disponível. Por favor, faça o upload na Página 1.")

if __name__ == '__main__':
    main()
