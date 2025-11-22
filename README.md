# Fique Segura

O Fique Segura é uma aplicação web que reúne dados oficiais de crimes de violência contra a mulher e apresenta essas informações para o usuário de forma clara, utilizando números, mapas e gráficos.

## Requisitos

* Python 3.10 ou superior
* Uv 0.8.2 ou superior

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/ppnunes/FiqueSegura.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd FiqueSegura
   ```
3. Instale as dependências com Uv:
   ```bash
   uv sync
   ```
4. Verifique se o Streamlit está instalado:
   ```bash
   uv run streamlit --version
   ```

## Execução

1. Execute a aplicação com o seguinte comando:
   ```bash
   uv run streamlit run main.py
   ```
2. Acesse a aplicação em seu navegador:
   * Abra um navegador e acesse `http://localhost:8501`
   * Você verá a página inicial da aplicação

## Desenvolvimento

* Para desenvolver a aplicação, você pode editar os arquivos `main.py` e `views/`
* Para adicionar novas páginas, crie um novo arquivo em `views/` e adicione o código necessário
* Para adicionar novas dependências, edite o arquivo `pyproject.toml` e adicione a dependência necessária

## Observações

* Certifique-se de que o Python e o Streamlit estejam instalados corretamente antes de executar a aplicação
* Se você tiver problemas para instalar as dependências, verifique se o arquivo `pyproject.toml` está correto e se as dependências estão disponíveis
* Se você tiver problemas para executar a aplicação, verifique se o arquivo `main.py` está correto e se as dependências estão instaladas corretamente

### Executando os Testes

1. Certifique-se de que todas as dependências estão instaladas:
   ```bash
   uv sync
   ```
2. Exporte o caminho do projeto para o `PYTHONPATH`:
   ```bash
   export PYTHONPATH=$(pwd)
   ```
3. Execute os testes com o seguinte comando:
   ```bash
   uv run pytest
   ```

### Testes de Carga e Stress com k6

O projeto inclui testes de carga e stress usando k6 para validar a performance e resiliência da aplicação.

#### Pré-requisitos

1. Instale o k6:
   ```bash
   # macOS (usando Homebrew)
   brew install k6
   
   # Ou baixe diretamente em https://k6.io/docs/get-started/installation/
   ```

2. Verifique a instalação:
   ```bash
   k6 version
   ```

#### Executando os Testes de Carga

1. Certifique-se de que a aplicação está rodando:
   ```bash
   uv run streamlit run main.py
   ```

2. Em outro terminal, execute o teste de carga:
   ```bash
   k6 run tests/k6_fiquesegura_load_test.js
   ```

3. Para especificar uma URL base diferente:
   ```bash
   k6 run -e BASE_URL=http://seu-servidor:8501 tests/k6_fiquesegura_load_test.js
   ```

#### Executando os Testes de Stress

1. Certifique-se de que a aplicação está rodando:
   ```bash
   uv run streamlit run main.py
   ```

2. Em outro terminal, execute o teste de stress:
   ```bash
   k6 run tests/k6_fiquesegura_stress_ui.js
   ```

3. Para especificar uma URL base diferente:
   ```bash
   k6 run -e BASE_URL=http://seu-servidor:8501 tests/k6_fiquesegura_stress_ui.js
   ```

#### Gerando Relatórios em HTML

Para gerar relatórios em HTML com os resultados:

```bash
# Teste de carga com saída em HTML
k6 run tests/k6_fiquesegura_load_test.js --out csv=load.csv
k6 run tests/k6_fiquesegura_load_test.js --out json=load.json

# Teste de stress com saída em HTML
k6 run tests/k6_fiquesegura_stress_ui.js --out csv=stress.csv
k6 run tests/k6_fiquesegura_stress_ui.js --out json=stress.json
```

Você pode utilizar também o  plugin [xk6-dashboard](https://github.com/grafana/xk6-dashboard) para ter uma boa visualização da saída.
#### Interpretando os Resultados

**Teste de Carga:**
- Valida que o sistema comporta até 2000 usuários simultâneos
- Verifica se p(95) < 500ms e p(99) < 1200ms
- Taxa de erro máxima permitida: < 1%

**Teste de Stress:**
- Simula aumento gradual de carga até 5000 usuários
- Verifica se p(95) < 1500ms e p(99) < 2000ms
- Taxa de erro máxima permitida: < 10%

Os testes executam requisições para:
- `GET /` - Página inicial
- `GET /?page=dados` - Página de dados
- `GET /favicon.ico` - Recurso estático

### Adicionando Novos Testes

1. Crie um novo arquivo de teste no diretório `tests/`. Por convenção, o nome do arquivo deve começar com `test_`, por exemplo, `test_novafuncionalidade.py`.
2. Escreva suas funções de teste no arquivo criado. Cada função de teste deve começar com `test_`.
3. Certifique-se de que os testes cobrem os cenários esperados e possíveis casos de erro.
4. Para verificar se os novos testes estão funcionando, execute novamente o comando:
   ```bash
   uv run pytest
   ```
