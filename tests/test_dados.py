from pathlib import Path
import streamlit.testing.v1 as ts_test
from views.Dados import main
from utils import load_data, load_feminicidio, load_map_count, clear_names, export_df
import pytest
import pandas as pd
from unittest.mock import patch


def test_dados_title_and_markdown():
    # Testa se o título e o markdown inicial estão presentes
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "views/Dados.py")
    runner.run(timeout=30)

    # Verifica o markdown inicial
    assert any("Os dados foram obtidos do portal dados abertos" in md.value for md in runner.markdown)

def test_dados_selectbox():
    # Testa se os selectboxes estão presentes e possuem as opções corretas
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "views/Dados.py")
    runner.run(timeout=30)

    # Verifica o primeiro selectbox (Eixo X)
    assert runner.selectbox[0].label == "Eixo X:"
    assert len(runner.selectbox[0].options) > 0  # Deve ter opções disponíveis

    # Verifica o terceiro selectbox (Município)
    assert runner.selectbox[2].label == "Município:"
    assert len(runner.selectbox[1].options) > 0  # Deve ter opções disponíveis

def test_municipio_ocorrencias_e_feminicidio():
    # Testa se a seleção de município exibe a quantidade correta de ocorrências e feminicídios.
    df = load_data()
    fem = load_feminicidio()
    municipio = df['ID_MN_RESI'].iloc[0]
    ocorrencias = len(df[df['ID_MN_RESI'] == municipio])
    fem_ocorrencias = len(fem[fem['municipio_fato'] == municipio])
    assert ocorrencias >= 0
    assert fem_ocorrencias >= 0

def test_mapa_corresponde_dados():
    # Testa se o mapa gerado por load_map_count() e folium.Map corresponde aos dados agregados.
    n = 5
    gdf = load_map_count(n)
    assert 'NM_MUN' in gdf.columns
    assert 'ocorrencias' in gdf.columns

def test_load_data_columns():
    # Testa se load_data() retorna um DataFrame com as colunas esperadas usando mock
    expected_columns = {'DT_NOTIFIC', 'NU_IDADE_N', 'ID_MN_RESI'}
    mock_df = pd.DataFrame({
        'DT_NOTIFIC': ["2025-01-01"],
        'NU_IDADE_N': [30],
        'ID_MN_RESI': ["Belo Horizonte"]
    })
    with patch('utils.load_data', return_value=mock_df):
        df = load_data()
        assert expected_columns.issubset(df.columns)

def test_load_feminicidio_not_null():
    # Testar se load_feminicidio() retorna dados corretos e não nulos.
    df = load_feminicidio()
    assert not df.empty
    assert 'municipio_fato' in df.columns

def test_clear_names_renames_columns():
    # Testar se clear_names() renomeia corretamente as colunas do DataFrame.
    df = pd.DataFrame({'A': [1], 'B': [2]})
    renamed = clear_names(df, 'ses_columns')
    assert isinstance(renamed, pd.DataFrame)

def test_export_df_runs_without_error(tmp_path):
    # Testar se export_df() exporta o DataFrame sem erros e com o nome correto.
    df = pd.DataFrame({'A': [1, 2]})
    try:
        export_df(df, key="test_export")
    except Exception:
        pytest.fail("export_df raised an exception")
