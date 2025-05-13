from pathlib import Path
import streamlit.testing.v1 as ts_test

def test_dados_file():
    # Testa se o arquivo Dados.py existe
    assert (Path(__file__).parent.parent / "pages/Dados.py").exists()

def test_dados_title_and_markdown():
    # Testa se o título e o markdown inicial estão presentes
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "pages/Dados.py")
    runner.run(timeout=30)

    # Verifica o markdown inicial
    assert any("Os dados foram obtidos do portal dados abertos" in md.value for md in runner.markdown)

def test_dados_selectbox():
    # Testa se os selectboxes estão presentes e possuem as opções corretas
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "pages/Dados.py")
    runner.run(timeout=30)

    # Verifica o primeiro selectbox (Eixo X)
    assert runner.selectbox[0].label == "Eixo X:"
    assert len(runner.selectbox[0].options) > 0  # Deve ter opções disponíveis

    # Verifica o segundo selectbox (Município)
    assert runner.selectbox[1].label == "Município:"
    assert len(runner.selectbox[1].options) > 0  # Deve ter opções disponíveis
