import streamlit as st
import pandas as pd
import numpy as np
from unidecode import unidecode
from  utils import load_data, init_page, load_feminicidio

init_page()
if'nlargest' not in st.session_state:
    st.session_state.nlargest=5

dados = load_data()
feminicidios = load_feminicidio()

st.markdown(f""" # Sobre os dados
            
Os dados foram obtidos do portal dados abertos e abordam os dados apresentados de {dados.DT_NOTIFIC.min().strftime('%d/%m/%Y')} até {dados.DT_NOTIFIC.max().strftime('%d/%m/%Y')}, tendo no total {len(dados)} ocorrências (média de  {len(dados)/(365*2):.2f} ocorrências por dia). Os dados são referentes **apenas** a Minas Gerais, visto a indisponibilidade dos demais estados em compartilhar estes dados.
""")
# st.table(dados.head()[['NU_IDADE_N','ID_MN_RESI','VIOL_SEXU', 'VIOL_PSICO']])

st.selectbox('Eixo X:', dados.columns, key='x', placeholder='Selecione uma coluna', index=2)

df_agregado = dados.groupby([st.session_state.x]).size().reset_index(name='Quantidade')
st.line_chart(df_agregado, x=st.session_state.x, y='Quantidade')

st.selectbox('Município:', sorted(dados.ID_MN_RESI.unique()), key='municipio_dados', placeholder='Selecione um Município')

st.text(f"Um total de {len(dados[dados['ID_MN_RESI']== st.session_state.municipio_dados])} ocorrências")
st.table(dados[dados['ID_MN_RESI'] == st.session_state.municipio_dados][['LES_AUTOP', 'VIOL_FISIC', 'VIOL_PSICO', 'VIOL_SEXU']].groupby(axis=1, level=0).apply(lambda x: x.value_counts().loc['Sim'].sum()))
st.text(f"Um total de {len(feminicidios[feminicidios['municipio_fato'] == unidecode(st.session_state.municipio_dados)])} tratados como feminicídio (tentado ou consumado)")
st.table(feminicidios[feminicidios.municipio_fato == unidecode(st.session_state.municipio_dados)].groupby(['tentado_consumado']).size().reset_index())

st.title(f"Os {st.session_state.nlargest} municípios com mais ocorrências")
st.slider('Selecione um valor', min_value=2, max_value=20, value=5,step=1, key='nlargest')
table_data = dados.ID_MN_RESI.value_counts(normalize=True).nlargest(st.session_state.nlargest)*100
table_data.name = 'Proporção(%)'
table_data = table_data.reset_index()
table_data = table_data.rename(columns={'ID_MN_RESI': 'Município'})
st.table(table_data)
