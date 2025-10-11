


import streamlit as st
import folium
from streamlit_folium import st_folium
from utils import init_page, load_data, load_map_data_by_mn, clear_names
from utils.manager import save_user_choice

def main():
    # Captura o ajs_anonymous_id do cookie usando streamlit_js_eval
    try:
        from streamlit_js_eval import get_cookie
        ajs_id = get_cookie('ajs_anonymous_id')
        if ajs_id and 'ajs_anonymous_id' not in st.session_state:
            st.session_state['ajs_anonymous_id'] = ajs_id
    except ImportError:
        st.warning('Para capturar o ajs_anonymous_id, instale o pacote streamlit-js-eval: pip install streamlit-js-eval')

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
            if gdf.empty or not hasattr(gdf, 'geometry') or gdf.geometry.is_empty.any():
                st.warning(f"Não foi possível exibir o mapa para o município '{st.session_state.municipio}'. Dados geográficos ausentes ou inválidos.")
            else:
                gdf_projected = gdf.to_crs(epsg=31983) # Projeção UTM para o Brasil
                centroide = gdf_projected.geometry.centroid # Obter o centroide do GeoDataFrame
                centroide = centroide.to_crs(epsg=4674) # Projeção geográfica original
                if centroide.x.isnull().any() or centroide.y.isnull().any():
                    st.warning(f"Não foi possível calcular o centroide para o município '{st.session_state.municipio}'.")
                else:
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

    # Callback para busca automática ao alterar município (após a primeira busca)
    def municipio_callback():
        if st.session_state.mostrar_mapa:
            buscar_callback()

    st.selectbox('Cidade/Município:', sorted(data['ID_MN_RESI'].unique()), key='municipio', placeholder='Selecione uma opção', on_change=municipio_callback)

    def buscar_callback():
        # Garante que o ajs_anonymous_id está atualizado
        ajs_id = st.session_state.get('ajs_anonymous_id', None)
        save_user_choice(
            estado=st.session_state.estado,
            municipio=st.session_state.municipio,
            ajs_anonymous_id=ajs_id
        )
        enable_map()

    if st.session_state.mostrar_mapa:
        st.button('Nova busca', on_click=disable_map)
    else:
        st.button('Buscar', on_click=buscar_callback, disabled=not st.session_state.municipio)

# Para rodar a tela Home, chame main()
