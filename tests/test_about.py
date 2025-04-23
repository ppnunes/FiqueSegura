from pathlib import Path
import streamlit.testing.v1 as ts_test

def test_sobre_file():
    # Testa se o arquivo existe
    assert Path(__file__).parent.parent / "pages" / "Sobre.py"

def test_sobre_app():
    # Testa se o app inicia corretamente
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "pages" / "Sobre.py")
    runner.run(timeout=30) # Precisamos de uma espera maior para o app carregar

    # Testa se o título está correto
    assert runner.title[0].value == "Fique Segura."
    # Testa se o conteúdo do markdown está correto
    assert any('O que é o Fique Segura?' in m.value for m in runner.markdown)

    # Testa se o estado inicial da variável de sessão é False
    assert runner.session_state.mostrar_mapa == False