from pathlib import Path
import streamlit.testing.v1 as ts_test

def test_home_file():
    # Testa se o arquivo existe
    assert Path(__file__).parent.parent / "_Home.py"

def test_home_app():
    # Testa se o app inicia corretamente
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "_Home.py")
    runner.run(timeout=30) # Precisamos de uma espera maior para o app carregar

     # Testa se o título está correto
    assert any("Fique Segura" in titles.value for titles in runner.title)
    
    # Testa se o conteúdo do markdown está correto
    assert any('Pesquise informações baseadas em dados de denuncias de violência contra a mulher.  Utilize os filtros abaixo para selecionar os dados que deseja visualizar.' in m.value for m in runner.markdown)

    # Testa se o estado inicial da variável de sessão é False
    assert runner.session_state.mostrar_mapa == False

    assert runner.info[0].value == "Selecione ao menos 1 campo:"

    # assert len(runner.selectbox) == 2
    assert runner.selectbox[0].label == "Estado:"
    assert runner.selectbox[1].label == "Cidade/Município:"

    # Verifica se os botões estão presentes
    assert any(button.label == "Buscar" for button in runner.button)

def test_buscar_button():
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "_Home.py").run()
    runner.button[0].click().run()
    runner.session_state.municipio = "Belo Horizonte"  # Simula a seleção de um município

    # Simula o clique no botão "Buscar"
    assert runner.session_state.mostrar_mapa is True
    runner.button[0].click().run()
    assert runner.session_state.mostrar_mapa is False

def test_mapa_container():
    runner = ts_test.AppTest.from_file(Path(__file__).parent.parent / "_Home.py")
    runner.session_state.municipio = "Belo Horizonte"  # Simula a seleção de um município
    runner.session_state.mostrar_mapa = True
    runner.run(timeout=30)

    assert any(
        "Um total de" in m.value and "ocorrências foram registradas" in m.value
        for m in runner.markdown
    )