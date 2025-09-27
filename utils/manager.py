import requests
import numpy as np
import matplotlib.pyplot as plt
import time
import streamlit as st

def logoff():
    col1, col2 = st.columns([8,1])
    with col2:
        if st.button("Sair", help="Fazer logoff"):
            st.session_state["logado_admin"] = False
            st.rerun()


def login():
    st.title("🔒 Login Administrativo")
    usuario = st.text_input("Usuário", value="admin")
    senha = st.text_input("Senha", type="password", value="1234")
    if st.button("Entrar"):
        if usuario == "admin" and senha == "1234":
            st.session_state["logado_admin"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def carregar_markdown_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        texto = response.text
        # Remove preâmbulo YAML se existir
        if texto.startswith('---'):
            partes = texto.split('---', 2)
            if len(partes) == 3:
                texto = partes[2].lstrip('\n')
        return texto
    except Exception as e:
        return f"Erro ao carregar markdown: {e}"