import geopandas as gpd
import folium
from streamlit_folium import st_folium
from utils import init_page, load_map_count
import streamlit as st

init_page()

st.slider('Selecione um valor', min_value=1, max_value=20, value=5,step=1, key='qnt_itens')
gdf = load_map_count(st.session_state.qnt_itens)

# # Criar o mapa
gdf_projected = gdf.to_crs(epsg=31983) # Projeção UTM para o Brasil
centroide = gdf_projected.geometry.centroid # Obter o centroide do GeoDataFrame
centroide = centroide.to_crs(epsg=4674) # Projeção geográfica original
zoom = 6 if st.session_state.qnt_itens > 1 else 10
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
st.table(gdf[['NM_MUN','ocorrencias']])