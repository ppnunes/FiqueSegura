import streamlit as st
from utils.sidebar import router, sidebar

# Obtém o query param 'page' usando st.query_params
params = st.query_params
valor = params.get("page", '').lower()

# Usa o valor do query param como fonte principal da navegação
if valor in router:
    pagina_escolhida = valor
else:
    pagina_escolhida = "home"

# Se o usuário clicar em um botão da sidebar, atualiza o query param
selecionada = sidebar()
if selecionada:
    st.query_params["page"] = selecionada
    pagina_escolhida = selecionada

# Exibe a página escolhida
router[pagina_escolhida]["page"].main()