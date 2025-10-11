import streamlit as st
from views import Admin, Home, Sobre, Dados


router = {
    'home': {
        'name': 'Início',
        'icon': ':material/home:',
        'page': Home,
        'hide': False
    },
    'dados': {
        'name': 'Dados',
        'icon': ':material/bar_chart:',
        'page': Dados,
        'hide': False
    },
    'sobre': {
        'name': 'Sobre',
        'icon': ':material/info:',
        'page': Sobre,
        'hide': False
    },
    'admin': {
        'name': 'Administrativo',
        'icon': ':material/lock:',
        'page': Admin,
        'hide': True
    }
}

def sidebar():
    st.sidebar.title('Fique Segura')
    selecionada = None
    for key, config in router.items():
        if not config.get('hide', False):
            if st.sidebar.button(
                type="tertiary",
                label=config['name'],
                icon=config['icon']
                ):
                selecionada = key
    return selecionada