import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd


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
    if 'nlargest' not in st.session_state:
        st.session_state.nlargest = 10
    if 'municipio_dados' not in st.session_state:
        st.session_state.municipio_dados = "Belo Horizonte"
    if 'municipio' not in st.session_state:
        st.session_state.municipio = None
    if'mostrar_mapa' not in st.session_state:
        st.session_state.mostrar_mapa = False
        st.session_state.estado = 'Minas Gerais'
        st.session_state.municipio = None
    if 'ses_columns' not in st.session_state:
        # Salva colunas no estado da sessão
        st.session_state.ses_columns = {
            'DT_NOTIFIC': 'Data da Notificação',
            'DT_NASC': 'Data de Nascimento',
            'NU_IDADE_N': 'Idade',
            'OUT_VEZES': 'Outras Vezes',
            'LES_AUTOP': 'Lesão Autoprovocada',
            'VIOL_FISIC': 'Violência Física',
            'VIOL_PSICO': 'Violência Psicológica',
            'VIOL_SEXU': 'Violência Sexual',
            'NUM_ENVOLV': 'Número de Envolvidos',
            'AUTOR_SEXO': 'Sexo do Autor',
            'ORIENT_SEX': 'Orientação Sexual',
            'IDENT_GEN': 'Identidade de Gênero',
            'LOCAL_OCOR': 'Local da Ocorrência',
            'ID_MN_RESI': 'Município',
            'CS_RACA': 'Cor/Raça',
            'CS_SEXO': 'Sexo',
        }
    if 'feminicidio_columns' not in st.session_state:
        # Salva colunas no estado da sessão
        st.session_state.feminicidio_columns = {
            'data_fato': 'Data do Fato',
            'municipio_fato': 'Município do Fato',
            'qtde_vitimas': 'Quantidade de Vítimas',
            'tentado_consumado': 'Tentado/Consumado',
            'municipio_cod': 'Código do Município',
            'mes': 'Mês',
            'ano': 'Ano',
            'risp': 'RISP',
            'rmbh': 'RMBH',
        }



@st.cache_data
def load_data() -> pd.DataFrame:
    """ Carrega os dados necessários para o projeto"""

    # Carrega os arquivos CSV e concatenas eles em um unico dataframe
    df = pd.read_csv('assets/dados_violencia_mulheres_ses_2021.csv', sep=';')
    df = pd.concat([df, pd.read_csv('assets/dados_violencia_mulheres_ses_2022.csv', sep=';')])
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

@st.cache_data
def load_feminicidio() -> pd.DataFrame:
    df = pd.read_csv('assets/feminicidio_2022.csv', sep=';')
    df = pd.concat([df, pd.read_csv('assets/feminicidio_2023.csv', sep=';')])
    df = pd.concat([df, pd.read_csv('assets/feminicidio_2021.csv', sep=';')])

    df.data_fato = pd.to_datetime(df.data_fato, format='%Y-%m-%d')
    # df.tentado_consumado = df.tentado_consumado.astype('category')
    df.qtde_vitimas = df.qtde_vitimas.astype(int)
    df.municipio_fato = df.municipio_fato.apply(lambda x: x.title())

    return df

@st.cache_data
def load_map_data() -> gpd.GeoDataFrame:
    shapefile_path = 'assets/municipios_2023.geojson'
    gdf = gpd.read_file(shapefile_path)
    if gdf.crs is None:
        gdf.set_crs(epsg=4674, inplace=True)
    return gdf

@st.cache_data
def load_map_count(limit:int = 0) -> gpd.GeoDataFrame:
    gdf = load_map_data()
    # municipios_grouped = data.groupby('ID_MN_RESI', observed=False).size().reset_index(name='ocorrencias')
    # gdf = gdf.merge(municipios_grouped, left_on='NM_MUN', right_on='ID_MN_RESI', how='inner')
    # gdf['ocorrencias'] = gdf['ocorrencias'].fillna(0)
    # gdf.ocorrencias = gdf.ocorrencias.astype(int)
    # gdf.to_file('assets/municipios_2023.geojson', driver='GeoJSON')
    gdf.sort_values(by='ocorrencias', inplace=True, ascending=False)
    if limit > 0:
        gdf = gdf[:limit]
    return gdf

@st.cache_data
def load_map_data_by_mn(municipality:str) -> gpd.GeoDataFrame:
    gdf = load_map_data()
    gdf = gdf[gdf['ID_MN_RESI'] == municipality]
    return gdf

def clear_names(df:pd.DataFrame|pd.Series|str, session_name:str) -> pd.DataFrame:
    """Traduze os nomes das colunas do dataframe para o português"""
    name_map = st.session_state.get(session_name, {})
    if isinstance(df, pd.DataFrame):
        df.columns = df.columns.map(lambda x: name_map[x] if x in name_map else x)
    elif isinstance(df, pd.Series):
        df = df.rename(name_map)
    elif isinstance(df, str):
        return name_map.get(df, df)
    else:
        st.toast('Nada')

    return df