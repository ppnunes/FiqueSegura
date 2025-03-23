import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv('assets/dados_violencia_mulheres_ses_2022.csv', sep=';')
    df = pd.concat([df, pd.read_csv('assets/dados_violencia_mulheres_ses_2023.csv', sep=';')])
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
    df.dropna(inplace=True)
    return df

if'nlargest' not in st.session_state:
    st.session_state.nlargest=5

dados = load_data()

st.markdown(f""" # Sobre os dados
            
Os dados foram obtidos do portal dados abertos e abordam os dados apresentados de {dados.DT_NOTIFIC.min().strftime('%d/%m/%Y')} até {dados.DT_NOTIFIC.max().strftime('%d/%m/%Y')}, tendo no total {len(dados)} ocorrências (média de  {len(dados)/(365*2):.2f} ocorrências por dia). Os dados são referentes **apenas** a Minas Gerais, visto a indisponibilidade dos demais estados em compartilhar estes dados.
""")
st.table(dados.head()[['NU_IDADE_N','ID_MN_RESI','VIOL_SEXU', 'VIOL_PSICO']])

st.selectbox('Eixo X:', dados.columns, key='x', placeholder='Selecione uma coluna', index=2)

df_agregado = dados.groupby([st.session_state.x]).size().reset_index(name='Quantidade')
st.line_chart(df_agregado, x=st.session_state.x, y='Quantidade')

st.selectbox('Município:', sorted(dados.ID_MN_RESI.unique()), key='municipio', placeholder='Selecione um Município')

st.text(f"Um total de {len(dados[dados['ID_MN_RESI']== st.session_state.municipio])} ocorrências")

st.title(f"Os {st.session_state.nlargest} estados com mais ocorrências")
st.slider('Selecione um valor', min_value=2, max_value=20, value=5,step=1, key='nlargest')
table_data = dados.ID_MN_RESI.value_counts(normalize=True).nlargest(st.session_state.nlargest)*100
table_data.name = 'Proporção(%)'
table_data = table_data.reset_index()
table_data = table_data.rename(columns={'ID_MN_RESI': 'Município'})
st.table(table_data)
