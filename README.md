# Fique Segura

O Fique Segura é uma aplicação web que reúne dados oficiais de crimes de violência contra a mulher e apresenta essas informações para o usuário de forma clara, utilizando números, mapas e gráficos.

## Requisitos

* Python 3.10 ou superior
* Poetry 1.8.3 ou superior

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/ppnunes/FiqueSegura.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd FiqueSegura
   ```
3. Instale as dependências com Poetry:
   ```bash
   poetry install
   ```
4. Verifique se o Streamlit está instalado:
   ```bash
   poetry run streamlit --version
   ```

## Execução

1. Execute a aplicação com o seguinte comando:
   ```bash
   poetry run streamlit run Home.py
   ```
2. Acesse a aplicação em seu navegador:
   * Abra um navegador e acesse `http://localhost:8501`
   * Você verá a página inicial da aplicação

## Desenvolvimento

* Para desenvolver a aplicação, você pode editar os arquivos `Home.py` e `pages/Sobre.py`
* Para adicionar novas páginas, crie um novo arquivo em `pages/` e adicione o código necessário
* Para adicionar novas dependências, edite o arquivo `pyproject.toml` e adicione a dependência necessária

## Observações

* Certifique-se de que o Python e o Streamlit estejam instalados corretamente antes de executar a aplicação
* Se você tiver problemas para instalar as dependências, verifique se o arquivo `pyproject.toml` está correto e se as dependências estão disponíveis
* Se você tiver problemas para executar a aplicação, verifique se o arquivo `Home.py` está correto e se as dependências estão instaladas corretamente

### Executando os Testes

1. Certifique-se de que todas as dependências estão instaladas:
   ```bash
   poetry install
   ```
2. Exporte o caminho do projeto para o `PYTHONPATH`:
   ```bash
   export PYTHONPATH=$(pwd)
   ```
3. Execute os testes com o seguinte comando:
   ```bash
   poetry run pytest
   ```

### Adicionando Novos Testes

1. Crie um novo arquivo de teste no diretório `tests/`. Por convenção, o nome do arquivo deve começar com `test_`, por exemplo, `test_novafuncionalidade.py`.
2. Escreva suas funções de teste no arquivo criado. Cada função de teste deve começar com `test_`.
3. Certifique-se de que os testes cobrem os cenários esperados e possíveis casos de erro.
4. Para verificar se os novos testes estão funcionando, execute novamente o comando:
   ```bash
   poetry run pytest
   ```
