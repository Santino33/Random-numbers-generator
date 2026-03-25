import streamlit as st

COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#28A745',
    'danger': '#DC3545',
    'warning': '#FFC107',
    'info': '#17A2B8',
    'dark': '#343A40',
    'light': '#F8F9FA',
    'background': '#FFFFFF',
    'card_bg': '#F8F9FA',
}

CHART_COLORS = [
    '#2E86AB', '#A23B72', '#28A745', '#DC3545', 
    '#FFC107', '#17A2B8', '#6F42C1', '#20C997',
    '#E83E8C', '#6610F2'
]

PAGE_CONFIG = {
    'page_title': 'Simulador de Números Aleatorios',
    'page_icon': '🎲',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

DEFAULT_PARAMS = {
    'congruencial_lineal': {
        'semilla': 12345,
        'a': 16807,
        'c': 0,
        'm': 2147483647,
        'n': 1000,
        'precision': 7
    },
    'congruencial_multiplicativo': {
        'semilla': 12345,
        'a': 16807,
        'm': 2147483647,
        'n': 1000,
        'precision': 7
    },
    'cuadrados_medios': {
        'semilla': 1234,
        'k': 4,
        'n': 100,
        'truncamiento': '2k'
    }
}

SIGNIFICANCE_LEVEL = 0.05

def init_session_state():
    if 'generators_results' not in st.session_state:
        st.session_state.generators_results = {}
    if 'test_results' not in st.session_state:
        st.session_state.test_results = {}
    if 'history' not in st.session_state:
        st.session_state.history = []

init_session_state()
