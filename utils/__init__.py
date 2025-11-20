

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import sqlite3
import io

def gdf_from_sqlite(table_name, db_name="cache.db", crs="EPSG:4674"):
    conn = get_sqlite_conn(db_name)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    if "geometry" in df.columns:
        df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=crs)
        return gdf
    return df

def get_sqlite_conn(db_name="cache.db"):
    return sqlite3.connect(db_name)

def df_to_sqlite(df, table_name, db_name="cache.db"):
    conn = get_sqlite_conn(db_name)
    # Se for GeoDataFrame, converte geometry para WKT
    if hasattr(df, 'geometry'):
        df = df.copy()
        df['geometry'] = df['geometry'].apply(lambda x: x.wkt if x is not None else None)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def df_from_sqlite(table_name, db_name="cache.db"):
    conn = get_sqlite_conn(db_name)
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    except Exception:
        df = None
    conn.close()
    return df

def gdf_from_sqlite(table_name, db_name="cache.db", crs="EPSG:4674"):
    import pandas as pd
    import geopandas as gpd
    conn = get_sqlite_conn(db_name)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    if "geometry" in df.columns:
        df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=crs)
        return gdf
    return df


def init_page(page_icon=":balloon:", layout="centered"):
    try:
        st.set_page_config(
            page_title="Fique Segura",
            page_icon=page_icon,
            layout=layout,
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
    """Carrega os dados necessários para o projeto, usando cache SQLite se disponível"""
    df = df_from_sqlite("violencia_ses")
    if df is not None and not df.empty:
        # Corrige tipos das colunas ao carregar do SQLite
        df.DT_NOTIFIC = pd.to_datetime(df.DT_NOTIFIC, errors='coerce')
        df.DT_NASC = pd.to_datetime(df.DT_NASC, errors='coerce')
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
        return df
    # Carrega os arquivos CSV e concatena em um único dataframe
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
    # Salva no SQLite para cache
    df_to_sqlite(df, "violencia_ses")
    return df


@st.cache_data
def load_feminicidio() -> pd.DataFrame:
    df = df_from_sqlite("feminicidio")
    if df is not None and not df.empty:
        return df
    df = pd.read_csv('assets/feminicidio_2022.csv', sep=';')
    df = pd.concat([df, pd.read_csv('assets/feminicidio_2023.csv', sep=';')])
    df = pd.concat([df, pd.read_csv('assets/feminicidio_2021.csv', sep=';')])
    df.data_fato = pd.to_datetime(df.data_fato, format='%Y-%m-%d')
    # df.tentado_consumado = df.tentado_consumado.astype('category')
    df.qtde_vitimas = df.qtde_vitimas.astype(int)
    df.municipio_fato = df.municipio_fato.apply(lambda x: x.title())
    # Salva no SQLite para cache
    df_to_sqlite(df, "feminicidio")
    return df

@st.cache_data
@st.cache_data
def load_map_data() -> gpd.GeoDataFrame:
    # Tenta carregar do cache SQLite
    try:
        gdf = gdf_from_sqlite("geojson")
        if gdf is not None and hasattr(gdf, "geometry"):
            return gdf
    except Exception:
        pass
    # Se não conseguir, carrega do arquivo
    shapefile_path = 'assets/municipios_2023.geojson'
    gdf = gpd.read_file(shapefile_path)
    if gdf.crs is None:
        gdf.set_crs(epsg=4674, inplace=True)
    # Salva no SQLite para cache
    df_to_sqlite(gdf, "geojson")
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

def export_df(df:pd.DataFrame|pd.Series|list, key:str):

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if isinstance(df, list):
            for i in df:
                i.to_excel(writer, index=False)
        else:
            df.to_excel(writer, index=False)
    output.seek(0)
    st.download_button(
        label="Exportar tabela",
        data=output,
        file_name="fiquesegura.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=key
    )

