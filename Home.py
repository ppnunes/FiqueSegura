import streamlit as st
import pandas as pd
import numpy as np
from pages.Dados import load_data
from utils import init_page, load_data

def enable_map():
    st.session_state.mostrar_mapa = True
    st.success('Mapa carregado com sucesso!')
    st.table(st.session_state)

def disable_map():
    st.session_state.mostrar_mapa = False

init_page()
data = load_data()

st.title('Fique Segura')

st.markdown("""
    Pesquise informações baseadas em dados de denuncias de violência contra a mulher.  Utilize os filtros abaixo para selecionar os dados que deseja visualizar.
""")

st.info('Selecione ao menos 1 campo:', icon="ℹ️")

mapa_container = st.container()
if st.session_state.mostrar_mapa:
    with mapa_container:
        st.map()

st.selectbox('Estado:', ['Opção 1', 'Opção 2', 'Opção 3'], key='estado', on_change=disable_map, placeholder='Selecione uma opção')
st.selectbox('Cidade:', ['Opção 1', 'Opção 2', 'Opção 3'], key='cidade', on_change=disable_map, placeholder='Selecione uma opção')
st.selectbox('Tipo de Crime:', ['Opção 1', 'Opção 2', 'Opção 3'], key='municipio', on_change=disable_map, placeholder='Selecione uma opção')

if st.session_state.mostrar_mapa:
    st.button('Nova busca', on_click=disable_map)
else:
    st.button('Buscar', on_click=enable_map,disabled=not st.session_state.estado or not st.session_state.cidade or not st.session_state.municipio)

# st.table(data.head()[['NU_IDADE_N','ID_MN_RESI','VIOL_SEXU', 'VIOL_PSICO']])