
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
    # st.markdown(carregar_markdown_url("https://raw.githubusercontent.com/ppnunes/Relatorios/refs/heads/teste_software/n1-fique-segura.md"))

    # st.markdown(carregar_markdown_url("https://raw.githubusercontent.com/ppnunes/Relatorios/refs/heads/teste_software/n1.md"))

    st.header('Relatório de Uso dos Usuários')
    # Quantidade de usuários únicos
    n_usuarios = count_unique_users()
    st.metric('Usuários únicos registrados', n_usuarios)

    # Relatório das escolhas mais comuns
    relatorio = get_most_common_choices(top_n=10)

    st.subheader('Municípios mais acessados (Top 10)')
    if relatorio['municipios']:
        # Ordena por quantidade (desc) e nome (asc)
        municipios_ordenados = sorted(relatorio['municipios'], key=lambda x: (-x[1], x[0]))
        import pandas as pd
        df_municipios = pd.DataFrame(municipios_ordenados, columns=['Município', 'Buscas'])
        st.table(df_municipios)
    else:
        st.write('Nenhum dado disponível.')

    st.subheader('Estados mais acessados (Top 10)')
    if relatorio['estados']:
        # Ordena por quantidade (desc) e nome (asc)
        estados_ordenados = sorted(relatorio['estados'], key=lambda x: (-x[1], x[0]))
        import pandas as pd
        df_estados = pd.DataFrame(estados_ordenados, columns=['Estado', 'Buscas'])
        st.table(df_estados)
    else:
        st.write('Nenhum dado disponível.')