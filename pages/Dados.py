import streamlit as st
import folium
from streamlit_folium import st_folium
from unidecode import unidecode
from  utils import *

init_page()

dados = load_data()
feminicidios = load_feminicidio()

st.markdown(f""" # Sobre os dados
            
Os dados foram obtidos do portal dados abertos e abordam os dados apresentados de {dados.DT_NOTIFIC.min().strftime('%d/%m/%Y')} até {dados.DT_NOTIFIC.max().strftime('%d/%m/%Y')}, tendo no total {len(dados)} ocorrências (média de  {len(dados)/(365*2):.2f} ocorrências por dia). Os dados são referentes **apenas** a Minas Gerais, visto a indisponibilidade dos demais estados em compartilhar estes dados.
""")
# st.table(dados.head()[['NU_IDADE_N','ID_MN_RESI','VIOL_SEXU', 'VIOL_PSICO']])
options_line = [
    'DT_NOTIFIC',
    'NU_IDADE_N',
    'ID_MN_RESI',
]

st.selectbox('Eixo X:', options_line, key='x', placeholder='Selecione uma coluna', index=2, format_func=lambda x: st.session_state.ses_columns[x] if x in st.session_state.ses_columns else x)

df_agregado = dados.groupby([st.session_state.x]).size().reset_index(name='Quantidade')
st.line_chart(df_agregado, x=st.session_state.x, y='Quantidade', x_label=st.session_state.ses_columns[st.session_state.x])

options_bar = [
    'VIOL_FISIC',
    'VIOL_PSICO',
    'VIOL_SEXU',
    'ORIENT_SEX',
    'LOCAL_OCOR',
    'CS_RACA',
]
st.selectbox('Eixo X:', options_bar, key='x_bar', placeholder='Selecione uma coluna', index=2, format_func=lambda x: st.session_state.ses_columns[x] if x in st.session_state.ses_columns else x)
df_agregado_bar = dados.groupby([st.session_state.x_bar]).size().reset_index(name='Quantidade')
st.bar_chart(df_agregado_bar, x=st.session_state.x_bar, y='Quantidade', x_label=st.session_state.ses_columns[st.session_state.x_bar])


st.selectbox('Município:', sorted(dados.ID_MN_RESI.unique()), key='municipio_dados', placeholder='Selecione um Município')

st.text(f"Um total de {len(dados[dados['ID_MN_RESI']== st.session_state.municipio_dados])} ocorrências")

table = dados[dados['ID_MN_RESI'] == st.session_state.municipio_dados][['LES_AUTOP', 'VIOL_FISIC', 'VIOL_PSICO', 'VIOL_SEXU','OUT_VEZES']].groupby(axis=1, level=0).apply(lambda x: x.value_counts().loc['Sim'].sum())
table = clear_names(table, 'ses_columns')
table.reset_index().columns = ['Tipo de Violência', 'Quantidade']
st.bar_chart(table, horizontal=True, use_container_width=True)

st.text(f"Um total de {len(feminicidios[feminicidios['municipio_fato'] == unidecode(st.session_state.municipio_dados)])} tratados como feminicídio (tentado ou consumado)")
# table = feminicidios[feminicidios.municipio_fato == unidecode(st.session_state.municipio_dados)].groupby(['tentado_consumado']).size().reset_index()
# table = clear_names(table, 'feminicidio_columns')
# table = table.rename(columns={0: 'Quantidade'})


st.title(f"Os {st.session_state.nlargest} municípios com mais ocorrências")
st.slider('Selecione um valor', min_value=2, max_value=20, step=1, key='nlargest')
table_data = dados.ID_MN_RESI.value_counts(normalize=True).nlargest(st.session_state.nlargest)*100
table_data.name = 'Proporção(%)'
table_data = table_data.reset_index()
table_data = table_data.rename(columns={'ID_MN_RESI': 'Município'})


# # Criar o mapa
gdf = load_map_count(st.session_state.nlargest)
gdf_projected = gdf.to_crs(epsg=31983) # Projeção UTM para o Brasil
centroide = gdf_projected.geometry.centroid # Obter o centroide do GeoDataFrame
centroide = centroide.to_crs(epsg=4674) # Projeção geográfica original
zoom = 6 if st.session_state.nlargest > 1 else 10
m = folium.Map(location=[centroide.y.mean(), centroide.x.mean()], zoom_start=zoom)  # Coordenadas aproximadas do Brasil

# # Adicionar o gráfico de calor
folium.Choropleth(
    geo_data=gdf,
    name='choropleth',
    data=gdf,
    columns=['NM_MUN', 'ocorrencias'],
    key_on='feature.properties.NM_MUN',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Ocorrências por Município'
).add_to(m)

# # Exibir o mapa no Streamlit
st_folium(m, width=700, height=500)

gdf.drop(columns=['geometry'], inplace=True)

st.table(table_data)
