import streamlit as st
import folium
from streamlit_folium import st_folium
from pages.Dados import load_data
from utils import init_page, load_data, load_map_data_by_mn, clear_names

def enable_map():
    st.session_state.mostrar_mapa = True

def disable_map():
    st.session_state.mostrar_mapa = False

init_page()
data = load_data()

st.title('Fique Segura')

st.markdown("""
    Pesquise informações baseadas em dados de denuncias de violência contra a mulher.  Utilize os filtros abaixo para selecionar os dados que deseja visualizar.
""")

st.info('Selecione ao menos 1 campo:', icon="ℹ️")

mapa_container = st.container()
if st.session_state.mostrar_mapa and 'municipio' in st.session_state and st.session_state.municipio:
    with mapa_container:
        gdf = load_map_data_by_mn(st.session_state.municipio)
        gdf_projected = gdf.to_crs(epsg=31983) # Projeção UTM para o Brasil
        centroide = gdf_projected.geometry.centroid # Obter o centroide do GeoDataFrame
        centroide = centroide.to_crs(epsg=4674) # Projeção geográfica original
        zoom = 10
        m = folium.Map(location=[centroide.y.mean(), centroide.x.mean()], zoom_start=zoom)  # Coordenadas aproximadas do Brasil
        folium.Choropleth(
            geo_data=gdf,
            name='choropleth',
            data=gdf,
            columns=['NM_MUN', 'ocorrencias'],
            key_on='feature.properties.NM_MUN',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            # legend_name='Ocorrências por Município'
        ).add_to(m)

        # # Exibir o mapa no Streamlit
        st_folium(m, width=700, height=500)
        cols = ['VIOL_FISIC', 'VIOL_PSICO', 'VIOL_SEXU']
        contagem = data[data['ID_MN_RESI'] == st.session_state.municipio][cols].apply(lambda x: (x == 'Sim').sum())
        col_mais_ocorrencias = clear_names(contagem.idxmax(), 'ses_columns')
        st.markdown('''
                    Um total de **{}** ocorrências foram registradas em **{}** entre {} e {}, sendo que a maior parte dos casos foram de **{}**.
                    '''.format(
                        gdf['ocorrencias'].sum(),
                        st.session_state.municipio,
                        data.DT_NOTIFIC.min().strftime('%Y'),
                        data.DT_NOTIFIC.max().strftime('%Y'),
                        col_mais_ocorrencias,
                        ))

st.selectbox('Estado:', ['Minas Gerais'], key='estado', on_change=disable_map, placeholder='Selecione uma opção', disabled=True)
st.selectbox('Cidade/Município:', sorted(data['ID_MN_RESI'].unique()), key='municipio', placeholder='Selecione uma opção')

if st.session_state.mostrar_mapa:
    st.button('Nova busca', on_click=disable_map)
else:
    st.button('Buscar', on_click=enable_map, disabled=not st.session_state.municipio)
