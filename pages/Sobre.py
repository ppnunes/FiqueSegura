import streamlit as st
from utils import init_page
import streamlit.components.v1 as components

init_page()
st.title('Fique Segura.')

st.markdown("""
## O que é o Fique Segura?

O Fique Segura é uma aplicação web dedicada à democratização do acesso a informações sobre crimes de violência contra a mulher no Brasil. O projeto foi desenvolvido para reunir, tratar e apresentar dados oficiais de forma clara, acessível e visual, promovendo a conscientização, o empoderamento e o apoio à tomada de decisões de gestoras, pesquisadoras e toda a sociedade.

A aplicação disponibiliza mapas interativos, gráficos e tabelas que permitem a consulta de estatísticas de violência de gênero segmentadas por município, estado, tipo de crime e faixa etária, tornando mais fácil identificar padrões e tendências regionais.

Todas as informações são provenientes de bases públicas e oficiais, respeitando princípios de privacidade e anonimização. As principais fontes de dados utilizadas atualmente são:
- [Dados Gerais de Violência - SES](https://dados.gov.br/dados/conjuntos-dados/dados_violencia_geral_ses)
- [Violência contra a Mulher - Feminicídio](https://dados.gov.br/dados/conjuntos-dados/violencia-contra-mulher)

O tratamento e análise dos dados seguem métodos transparentes e documentados, com processamento realizado por scripts Python, conforme detalhado na documentação do projeto. As informações são atualizadas conforme a disponibilização de novos conjuntos de dados pelas fontes oficiais.

O Fique Segura busca impactar positivamente a sociedade ao centralizar e simplificar o acesso a dados críticos sobre violência de gênero, contribuindo para a prevenção, o combate à violência contra a mulher e o desenvolvimento de políticas públicas mais efetivas.
""")

st.markdown("""
---

## Como funciona a aplicação?

A aplicação Fique Segura foi desenvolvida utilizando a tecnologia Streamlit, focando em praticidade, transparência e acessibilidade. Os dados públicos são processados por scripts Python, que realizam o pré-processamento e a limpeza dos arquivos CSV obtidos das fontes oficiais. Esses dados tratados são carregados automaticamente quando a aplicação é acessada.

Na página principal, o fluxo de funcionamento ocorre da seguinte forma:
- O usuário acessa a interface web;
- A aplicação carrega os dados já processados e disponibiliza ferramentas de visualização (mapas, gráficos e filtros interativos);
- O usuário pode interagir com filtros para refinar a visualização dos dados;
- A cada interação, a aplicação atualiza dinamicamente as visualizações conforme o contexto escolhido.

O diagrama de sequência abaixo ilustra esse fluxo de funcionamento da página principal:
""")

mermaid_code = """
<div class="mermaid">
sequenceDiagram
    participant Usuário
    participant Navegador
    participant Streamlit App
    participant Scripts de Dados

    Usuário->>Navegador: Acessa a página principal
    Navegador->>Streamlit App: Envia requisição HTTP (GET)
    Streamlit App->>Scripts de Dados: Carrega e processa arquivos CSV (cache/local)
    Scripts de Dados-->>Streamlit App: Retorna DataFrames prontos para uso
    Streamlit App->>Navegador: Renderiza interface principal (mapas, gráficos, filtros)
    Navegador-->>Usuário: Exibe dashboard interativo
    Usuário->>Navegador: Interage com filtros, mapas e gráficos
    Navegador->>Streamlit App: Envia parâmetros/ações do usuário
    Streamlit App->>Scripts de Dados: Filtra/atualiza dados conforme interação
    Scripts de Dados-->>Streamlit App: Retorna dados filtrados
    Streamlit App->>Navegador: Atualiza visualizações na interface
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({startOnLoad:true});
</script>
"""

components.html(mermaid_code, height=400, scrolling=True)


st.markdown("""
---

## Responsável pelo desenvolvimento

Esta ferramenta foi idealizada, desenvolvida e é mantida por Priscila Nunes.

Para mais informações, dúvidas ou sugestões, entre em contato pelo GitHub: [ppnunes](https://github.com/ppnunes)
""")
