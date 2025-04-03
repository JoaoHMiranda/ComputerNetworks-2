import streamlit as st

def main():
    st.title("Formulário com Validação e Resultados")

    default_nome = ""
    default_idade = 25
    default_cores = []

    with st.form("formulario"):
        nome = st.text_input("Nome", value=default_nome, key="nome")
        idade = st.number_input("Idade", min_value=0, max_value=120, value=default_idade, key="idade")
        cores = st.multiselect(
            "Preferência de cor",
            options=["Vermelho", "Azul", "Verde", "Amarelo", "Roxo", "Laranja"],
            default=default_cores,
            key="cores"
        )

        col1, col2 = st.columns(2)
        submit_button = col1.form_submit_button("Enviar")
        clear_button = col2.form_submit_button("Limpar Formulário")

    if clear_button:
        # Remove os valores dos widgets do session_state
        for key in ["nome", "idade", "cores"]:
            if key in st.session_state:
                del st.session_state[key]
        # Força a atualização da página com meta refresh
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

    if submit_button:
        if not nome:
            st.error("Por favor, insira seu nome.")
        elif idade < 0 or idade > 120:
            st.error("A idade deve estar entre 0 e 120.")
        else:
            cores_str = ", ".join(cores) if cores else "nenhuma cor selecionada"
            st.success(f"Olá, {nome}, com {idade} anos, você gosta de {cores_str}!")

if __name__ == '__main__':
    main()
