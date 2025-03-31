import streamlit as st
import pandas as pd
import numpy as np


def init_page():
    try:
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
    except:
        pass
    # Inicialize a variável de sessão como False
    if'mostrar_mapa' not in st.session_state:
        st.session_state.mostrar_mapa = False
        st.session_state.estado = None
        st.session_state.cidade = None
        st.session_state.municipio = None


@st.cache_data
def load_data() -> pd.DataFrame:
    """ Carrega os dados necessários para o projeto"""

    # Carrega os arquivos CSV e concatenas eles em um unico dataframe
    df = pd.read_csv('assets/dados_violencia_mulheres_ses_2022.csv', sep=';')
    df = pd.concat([df, pd.read_csv('assets/dados_violencia_mulheres_ses_2023.csv', sep=';')])

    # Converte as colunas para os tipos corretos
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

    # remove qualquer linha que possa contar dados nulos ainda
    df.dropna(inplace=True)
    return df