
import streamlit as st
from utils.manager import *

st.set_page_config(page_title="Administração", page_icon="🔒", layout="wide")

if "logado_admin" not in st.session_state:
    st.session_state["logado_admin"] = False

if not st.session_state["logado_admin"]:
    login()
else:
    # Botão de logoff no canto superior direito
    logoff()
    # animacao()
    st.markdown(carregar_markdown_url("https://raw.githubusercontent.com/ppnunes/Relatorios/refs/heads/teste_software/n1-fique-segura.md"))

    st.markdown(carregar_markdown_url("https://raw.githubusercontent.com/ppnunes/Relatorios/refs/heads/teste_software/n1.md"))