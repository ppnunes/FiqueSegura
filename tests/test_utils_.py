import pytest
import pandas as pd
import geopandas as gpd
from utils import (
    get_sqlite_conn, df_to_sqlite, df_from_sqlite, gdf_from_sqlite,
    load_data, load_feminicidio, load_map_data, load_map_count, load_map_data_by_mn,
    clear_names, export_df
)

# Testa se a função retorna uma conexão válida com o banco SQLite
def test_get_sqlite_conn_returns_connection(tmp_path):
    db_path = tmp_path / "test.db"
    conn = get_sqlite_conn(str(db_path))
    assert conn is not None
    conn.close()

# Testa se um DataFrame pode ser salvo e recuperado do banco SQLite corretamente
def test_df_to_sqlite_and_df_from_sqlite(tmp_path):
    db_path = tmp_path / "test.db"
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df_to_sqlite(df, "test_table", str(db_path))
    loaded_df = df_from_sqlite("test_table", str(db_path))
    assert loaded_df is not None
    assert set(loaded_df.columns) == set(df.columns)
    assert len(loaded_df) == 2

# Testa se a função clear_names renomeia corretamente as colunas de um DataFrame usando o dicionário salvo na sessão
def test_clear_names_dataframe(monkeypatch):
    df = pd.DataFrame({'A': [1], 'B': [2]})
    monkeypatch.setitem(__import__('streamlit').session_state, 'test_map', {'A': 'Coluna A', 'B': 'Coluna B'})
    result = clear_names(df, 'test_map')
    assert 'Coluna A' in result.columns
    assert 'Coluna B' in result.columns

# Testa se a função clear_names retorna o nome traduzido ao receber uma string como entrada
def test_clear_names_string(monkeypatch):
    monkeypatch.setitem(__import__('streamlit').session_state, 'test_map', {'A': 'Coluna A'})
    result = clear_names('A', 'test_map')
    assert result == 'Coluna A'

# Testa integração entre df_to_sqlite e df_from_sqlite para DataFrame
def test_salvar_e_carregar_dataframe_sqlite(tmp_path):
    db_path = tmp_path / "test.db"
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df_to_sqlite(df, "tabela_teste", str(db_path))
    df_carregado = df_from_sqlite("tabela_teste", str(db_path))
    assert df_carregado.equals(df)

# Testa integração entre df_to_sqlite e gdf_from_sqlite para GeoDataFrame
def test_salvar_e_carregar_gdf_sqlite(tmp_path):
    db_path = tmp_path / "test.db"
    gdf = gpd.GeoDataFrame({'A': [1]}, geometry=gpd.points_from_xy([0], [0]), crs="EPSG:4674")
    df_to_sqlite(gdf, "geo_tabela", str(db_path))
    gdf_carregado = gdf_from_sqlite("geo_tabela", str(db_path))
    assert isinstance(gdf_carregado, gpd.GeoDataFrame)
    assert 'geometry' in gdf_carregado.columns

# Testa se load_data retorna dados e se as colunas estão corretas após integração com clear_names
def test_carregar_dados_e_traduzir_coluna(monkeypatch):
    df = load_data()
    monkeypatch.setitem(__import__('streamlit').session_state, 'ses_columns', {'NU_IDADE_N': 'Idade'})
    nome_coluna = clear_names('NU_IDADE_N', 'ses_columns')
    assert nome_coluna == 'Idade'
    assert 'NU_IDADE_N' in df.columns

# Testa se load_feminicidio retorna dados e se a coluna municipio_fato está presente
def test_carregar_feminicidio_e_verificar_coluna():
    df = load_feminicidio()
    assert not df.empty
    assert 'municipio_fato' in df.columns

# Testa se load_map_data retorna um GeoDataFrame válido e se pode ser filtrado por município
def test_carregar_mapa_e_filtrar_por_municipio():
    gdf = load_map_data()
    municipio = gdf['ID_MN_RESI'].iloc[0]
    gdf_filtrado = load_map_data_by_mn(municipio)
    assert not gdf_filtrado.empty
    assert all(gdf_filtrado['ID_MN_RESI'] == municipio)

# Testa se load_map_count retorna os municípios ordenados por ocorrências e respeita o limite
def test_contagem_municipios_mais_incidentes():
    gdf = load_map_count(limit=3)
    assert len(gdf) == 3
    ocorrencias = gdf['ocorrencias'].tolist()
    assert ocorrencias == sorted(ocorrencias, reverse=True)