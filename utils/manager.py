import streamlit as st
import sqlite3
from datetime import datetime

def logoff():
    col1, col2 = st.columns([8,1])
    with col2:
        if st.button("Sair", help="Fazer logoff"):
            st.session_state["logado_admin"] = False
            st.rerun()


def login():
    st.title("🔒 Login Administrativo")
    col1, col2 = st.columns([2,1])
    with col1:
        usuario = st.text_input("Usuário", value="admin", placeholder="Usuário", help="Digite seu usuário", key="login_usuario")
        senha = st.text_input("Senha", type="password", value="1234", placeholder="Senha", help="Digite sua senha", key="login_senha")
        col_btn1, col_btn2 = st.columns([5,1])
        with col_btn2:
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


def save_user_choice(estado, municipio, ajs_anonymous_id, db_name="cache.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT,
            municipio TEXT,
            timestamp TEXT,
            ajs_anonymous_id TEXT
        )
    ''')
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO user_choices (estado, municipio, timestamp, ajs_anonymous_id)
        VALUES (?, ?, ?, ?)
    ''', (estado, municipio, timestamp, ajs_anonymous_id))
    conn.commit()
    conn.close()

# Função para contar usuários únicos
def count_unique_users(db_name="cache.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(DISTINCT ajs_anonymous_id) FROM user_choices WHERE ajs_anonymous_id IS NOT NULL
        ''')
        result = cursor.fetchone()[0]
    except sqlite3.OperationalError:
        result = 0
    conn.close()
    return result

# Função para gerar relatório das escolhas mais comuns
def get_most_common_choices(db_name="cache.db", top_n=10):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT municipio, COUNT(*) as total FROM user_choices
            WHERE municipio IS NOT NULL
            GROUP BY municipio
            ORDER BY total DESC
            LIMIT ?
        ''', (top_n,))
        municipios = cursor.fetchall()
        cursor.execute('''
            SELECT estado, COUNT(*) as total FROM user_choices
            WHERE estado IS NOT NULL
            GROUP BY estado
            ORDER BY total DESC
            LIMIT ?
        ''', (top_n,))
        estados = cursor.fetchall()
    except sqlite3.OperationalError:
        municipios = []
        estados = []
    conn.close()
    return {
        "municipios": municipios,
        "estados": estados
    }