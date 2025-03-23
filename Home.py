import streamlit as st
import pandas as pd
import numpy as np

def enable_map():
    st.session_state.mostrar_mapa = True
    st.success('Mapa carregado com sucesso!')
    st.table(st.session_state)

def disable_map():
    st.session_state.mostrar_mapa = False

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv('assets/dados_violencia_mulheres_ses_2022.csv', sep=';')
    df = pd.concat([df, pd.read_csv('assets/dados_violencia_mulheres_ses_2023.csv', sep=';')])
    df.DT_NOTIFIC = pd.to_datetime(df.DT_NOTIFIC, format='%d/%m/%Y')
    df.DT_NASC = pd.to_datetime(df.DT_NASC, format='%d/%m/%Y')
    df.replace({'NU_IDADE_N': {np.nan: -1}}, inplace=True)
    df.NU_IDADE_N = df.NU_IDADE_N.astype(int)
    df.OUT_VEZES = df.OUT_VEZES.astype('category')
    df.LES_AUTOP = df.LES_AUTOP.astype('category')
    df.VIOL_FISIC = df.VIOL_FISIC.astype('category')
    df.VIOL_PSICO = df.VIOL_PSICO.astype('category')
    df.VIOL_SEXU = df.VIOL_SEXU.astype('category')
    df.NUM_ENVOLV = df.NUM_ENVOLV.astype('category')
    df.AUTOR_SEXO = df.AUTOR_SEXO.astype('category')
    df.ORIENT_SEX = df.ORIENT_SEX.astype('category')
    df.IDENT_GEN = df.IDENT_GEN.astype('category')
    df.LOCAL_OCOR = df.LOCAL_OCOR.astype('category')
    df.ID_MN_RESI = df.ID_MN_RESI.astype('category')
    df.CS_RACA = df.CS_RACA.astype('category')
    df.CS_SEXO = df.CS_SEXO.astype('category')
    df.dropna(inplace=True)
    return df

st.set_page_config(
    page_title="Fique Segura",
    page_icon=":balloon:",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """# O que é o Fique Segura?
O Fique Segura é um aplicativo que tem como objetivo auxiliar mulheres vítimas de violência."""
    }
)
data = load_data()
# Inicialize a variável de sessão como False
if'mostrar_mapa' not in st.session_state:
    st.session_state.mostrar_mapa = False
    st.session_state.estado = None
    st.session_state.cidade = None
    st.session_state.municipio = None

st.title('Fique Segura!')

st.markdown("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
""")

st.info('Lorem ipsum dolor sit amet', icon="ℹ️")

mapa_container = st.container()
if st.session_state.mostrar_mapa:
    with mapa_container:
        st.map()

st.selectbox('Estado:', ['Opção 1', 'Opção 2', 'Opção 3'], key='estado', on_change=disable_map, placeholder='Selecione uma opção')
st.selectbox('Cidade:', ['Opção 1', 'Opção 2', 'Opção 3'], key='cidade', on_change=disable_map, placeholder='Selecione uma opção')
st.selectbox('Município:', ['Opção 1', 'Opção 2', 'Opção 3'], key='municipio', on_change=disable_map, placeholder='Selecione uma opção')

if st.session_state.mostrar_mapa:
    st.button('Nova busca', on_click=disable_map)
else:
    st.button('Buscar', on_click=enable_map,disabled=not st.session_state.estado or not st.session_state.cidade or not st.session_state.municipio)

st.table(data.head()[['NU_IDADE_N','ID_MN_RESI','VIOL_SEXU', 'VIOL_PSICO']])