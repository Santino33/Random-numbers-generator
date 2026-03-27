import streamlit as st
import numpy as np
import pandas as pd
import random
import time
from typing import List, Dict, Any

from generators import CongruencialLineal, CongruencialMultiplicativo, CuadradosMedios
from tests import ChiCuadrada, PruebaPoker, KolmogorovSmirnov
from visualization import AnimatedCharts, ComparisonCharts, InteractiveCharts
from config.settings import (
    COLORS, CHART_COLORS, PAGE_CONFIG, 
    DEFAULT_PARAMS, SIGNIFICANCE_LEVEL
)

st.set_page_config(**PAGE_CONFIG)

st.set_option('client.showSidebarNavigation', True)

st.markdown("""
<style>
    .main-header {
        font-size: 60px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #2E86AB 0%, #1a5276 100%);
        border-radius: 15px;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #343A40;
        margin-top: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
        border-radius: 5px;
        margin: 1rem 0;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
        border-radius: 5px;
        margin: 1rem 0;
        color: #721C24;
    }
    .info-box {
        padding: 1rem;
        background-color: #D1ECF1;
        border-left: 5px solid #17A2B8;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def sidebar_generators():
    """Sidebar para configuración de generadores"""
    st.sidebar.header("⚙️ Configuración")
    
    generador = st.sidebar.selectbox(
        "🎲 Seleccionar Generador",
        ["Congruencial Lineal", "Congruencial Multiplicativo", "Cuadrados Medios"],
        index=0
    )
    
    return generador


def config_lineal():
    """Configuración para generador congruencial lineal"""
    st.subheader("📝 Parámetros - Congruencial Lineal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        semilla = st.number_input(
            "Semilla (X₀)", 
            value=DEFAULT_PARAMS['congruencial_lineal']['semilla'],
            min_value=0,
            step=1,
            help="Valor inicial de la secuencia"
        )
        a = st.number_input(
            "Multiplicador (a)", 
            value=DEFAULT_PARAMS['congruencial_lineal']['a'],
            min_value=1,
            step=1,
            help="Constante multiplicadora"
        )
    
    with col2:
        c = st.number_input(
            "Incremento (c)", 
            value=DEFAULT_PARAMS['congruencial_lineal']['c'],
            min_value=0,
            step=1,
            help="Constante aditiva"
        )
        m = st.number_input(
            "Módulo (m)", 
            value=DEFAULT_PARAMS['congruencial_lineal']['m'],
            min_value=2,
            step=1,
            help="Módulo de la congruencia"
        )
    
    n = st.slider("Cantidad de números", 10, 10000, 1000, help="Cantidad de números a generar")
    precision = st.slider("Precisión (decimales)", 1, 10, 7)
    
    return {
        'semilla': int(semilla),
        'a': int(a),
        'c': int(c),
        'm': int(m),
        'n': int(n),
        'precision': int(precision)
    }


def config_multiplicativo():
    """Configuración para generador congruencial multiplicativo"""
    st.subheader("📝 Parámetros - Congruencial Multiplicativo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        semilla = st.number_input(
            "Semilla (X₀)", 
            value=DEFAULT_PARAMS['congruencial_multiplicativo']['semilla'],
            min_value=1,
            step=1,
            help="Valor inicial (debe ser impar para período completo)"
        )
        a = st.number_input(
            "Multiplicador (a)", 
            value=DEFAULT_PARAMS['congruencial_multiplicativo']['a'],
            min_value=1,
            step=1,
            help="Constante multiplicadora"
        )
    
    with col2:
        m = st.number_input(
            "Módulo (m)", 
            value=DEFAULT_PARAMS['congruencial_multiplicativo']['m'],
            min_value=2,
            step=1,
            help="Módulo de la congruencia"
        )
        n = st.slider("Cantidad de números", 10, 10000, 1000)
    
    precision = st.slider("Precisión (decimales)", 1, 10, 7)
    
    return {
        'semilla': int(semilla),
        'a': int(a),
        'm': int(m),
        'n': int(n),
        'precision': int(precision)
    }


def config_cuadrados():
    """Configuración para generador de cuadrados medios"""
    st.subheader("📝 Parámetros - Cuadrados Medios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        semilla = st.number_input(
            "Semilla (X₀)", 
            value=DEFAULT_PARAMS['cuadrados_medios']['semilla'],
            min_value=1,
            step=1,
            help="Valor inicial (k dígitos)"
        )
        k = st.slider(
            "Dígitos (k)", 2, 10, 4,
            help="Cantidad de dígitos a utilizar"
        )
    
    with col2:
        truncamiento = st.selectbox(
            "Truncamiento",
            ["2k", "k"],
            index=0,
            help="'2k': tomar 2k dígitos centrales, 'k': tomar k dígitos centrales"
        )
        n = st.slider("Cantidad de números", 10, 1000, 100)
    
    return {
        'semilla': int(semilla),
        'k': int(k),
        'truncamiento': truncamiento,
        'n': int(n)
    }


def display_metrics(stats: Dict[str, Any]):
    """Muestra las métricas en tarjetas"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Media", f"{stats.get('media', 0):.6f}")
    with col2:
        st.metric("Varianza", f"{stats.get('varianza', 0):.6f}")
    with col3:
        st.metric("Desviación", f"{stats.get('desviacion', 0):.6f}")
    with col4:
        st.metric("Mín", f"{stats.get('min', 0):.4f}")
    with col5:
        st.metric("Máx", f"{stats.get('max', 0):.4f}")
    
    if stats.get('periodo'):
        st.info(f"📊 Período detectado: {stats['periodo']}")


def display_test_results(result: Dict[str, Any], test_name: str):
    """Muestra los resultados de una prueba"""
    with st.expander(f"📈 {test_name}", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Estadístico", f"{result['estadistico']:.6f}")
        with col2:
            st.metric("Valor Crítico", f"{result['valor_critico']:.6f}")
        with col3:
            st.metric("p-valor", f"{result['p_valor']:.6f}")
        
        if result['pasa']:
            st.markdown(f"""
            <div class="success-box">
                <strong>✓ PASA</strong><br>
                {result['interpretacion']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="error-box">
                <strong>✗ NO PASA</strong><br>
                {result['interpretacion']}
            </div>
            """, unsafe_allow_html=True)


def run_tests(numeros: List[float], nivel_significancia: float = 0.05):
    """Ejecuta todas las pruebas estadísticas"""
    resultados = {}
    
    with st.spinner("Ejecutando pruebas estadísticas..."):
        chi2 = ChiCuadrada(numeros, nivel_significancia)
        resultados['chi_cuadrada'] = chi2.ejecutar()
        
        poker = PruebaPoker(numeros, nivel_significancia)
        resultados['poker'] = poker.ejecutar()
        
        ks = KolmogorovSmirnov(numeros, nivel_significancia)
        resultados['kolmogorov_smirnov'] = ks.ejecutar()
    
    return resultados


def main():
    st.markdown('''
    <p class="main-header">🎲 Simulador de Números Aleatorios</p>
    <p style="font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem;">
        Generadores Congruenciales • Cuadrados Medios • Pruebas Estadísticas
    </p>
    ''', unsafe_allow_html=True)
    
    generador = sidebar_generators()
    
    if generador == "Congruencial Lineal":
        params = config_lineal()
        
        if st.button("🚀 Generar Números", type="primary"):
            try:
                gen = CongruencialLineal(**params)
                numeros = gen.generar()
                stats = gen.get_estadisticas()
                
                st.session_state['numeros'] = numeros
                st.session_state['stats'] = stats
                st.session_state['generador_nombre'] = "Congruencial Lineal"
                st.session_state['params'] = params
                
                st.success(f"✅ Generados {params['n']} números aleatorios")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif generador == "Congruencial Multiplicativo":
        params = config_multiplicativo()
        
        if st.button("🚀 Generar Números", type="primary"):
            try:
                gen = CongruencialMultiplicativo(**params)
                numeros = gen.generar()
                stats = gen.get_estadisticas()
                
                st.session_state['numeros'] = numeros
                st.session_state['stats'] = stats
                st.session_state['generador_nombre'] = "Congruencial Multiplicativo"
                st.session_state['params'] = params
                
                st.success(f"✅ Generados {params['n']} números aleatorios")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif generador == "Cuadrados Medios":
        params = config_cuadrados()
        
        if st.button("🚀 Generar Números", type="primary"):
            try:
                gen = CuadradosMedios(**params)
                numeros = gen.generar()
                stats = gen.get_estadisticas()
                
                st.session_state['numeros'] = numeros
                st.session_state['stats'] = stats
                st.session_state['generador_nombre'] = "Cuadrados Medios"
                st.session_state['params'] = params
                
                st.success(f"✅ Generados {params['n']} números aleatorios")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    if 'numeros' in st.session_state:
        st.divider()
        
        st.subheader("📊 Estadísticas Descriptivas")
        display_metrics(st.session_state['stats'])
        
        st.divider()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Datos", "📈 Visualización", "🧪 Pruebas", "🔬 Comparación"])
        
        with tab1:
            st.subheader("Números Generados")
            
            df = pd.DataFrame({
                'Índice': range(len(st.session_state['numeros'])),
                'Ri': st.session_state['numeros']
            })
            
            st.dataframe(df, use_container_width=True, height=300)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "💾 Descargar CSV",
                csv,
                "numeros_aleatorios.csv",
                "text/csv"
            )
        
        with tab2:
            st.subheader("Visualizaciones")
            
            viz_type = st.selectbox(
                "Tipo de Visualización",
                ["Histograma", "ECDF", "Q-Q", "Correlación", "Frecuencia Dígitos", "Animación Histograma"]
            )
            
            if viz_type == "Histograma":
                fig = InteractiveCharts.create_histogram(st.session_state['numeros'])
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "ECDF":
                fig = InteractiveCharts.create_ecdf(st.session_state['numeros'])
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Q-Q":
                fig = InteractiveCharts.create_qq_plot(st.session_state['numeros'])
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Correlación":
                fig = ComparisonCharts.create_correlation_plot(st.session_state['numeros'])
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Frecuencia Dígitos":
                fig = InteractiveCharts.create_digit_frequency(st.session_state['numeros'])
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Animación Histograma":
                fig = AnimatedCharts.create_histogram_animation(st.session_state['numeros'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Pruebas de Aleatoriedad")
            
            nivel_sign = st.slider(
                "Nivel de Significancia (α)",
                0.01, 0.10, 0.05, 0.01
            )
            
            if st.button("▶ Ejecutar Pruebas"):
                resultados = run_tests(st.session_state['numeros'], nivel_sign)
                st.session_state['resultados'] = resultados
            
            if 'resultados' in st.session_state:
                resultados = st.session_state['resultados']
                
                st.markdown("### Chi-Cuadrada")
                display_test_results(resultados['chi_cuadrada'], "Chi-Cuadrada")
                
                with st.expander("Ver frecuencias"):
                    df_chi = pd.DataFrame({
                        'Intervalo': [f"{i[0]:.2f}-{i[1]:.2f}" for i in resultados['chi_cuadrada']['intervalos']],
                        'Observada': resultados['chi_cuadrada']['frecuencias_observadas'],
                        'Esperada': resultados['chi_cuadrada']['frecuencias_esperadas']
                    })
                    st.dataframe(df_chi, use_container_width=True)
                
                st.markdown("### Prueba Poker")
                display_test_results(resultados['poker'], "Poker")
                
                with st.expander("Ver frecuencias"):
                    df_poker = pd.DataFrame({
                        'Categoría': list(resultados['poker']['frecuencias_observadas'].keys()),
                        'Observada': list(resultados['poker']['frecuencias_observadas'].values()),
                        'Esperada': list(resultados['poker']['frecuencias_esperadas'].values())
                    })
                    st.dataframe(df_poker, use_container_width=True)
                
                st.markdown("### Kolmogorov-Smirnov")
                display_test_results(resultados['kolmogorov_smirnov'], "Kolmogorov-Smirnov")
                
                with st.expander("Ver comparación con scipy"):
                    chi2 = ChiCuadrada(st.session_state['numeros'], nivel_sign)
                    comp_chi = chi2.comparar_scipy()
                    st.json(comp_chi)
                    
                    ks = KolmogorovSmirnov(st.session_state['numeros'], nivel_sign)
                    comp_ks = ks.comparar_scipy()
                    st.json(comp_ks)
        
        with tab4:
            st.subheader("Comparación con Bibliotecas")
            
            if st.button("▶ Comparar con numpy.random"):
                np.random.seed(42)
                numpy_nums = list(np.random.random(len(st.session_state['numeros'])))
                st.session_state['numpy_nums'] = numpy_nums
            
            if 'numpy_nums' in st.session_state:
                fig = ComparisonCharts.compare_with_libraries(
                    st.session_state['numeros'],
                    st.session_state['numpy_nums']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Estadísticas Personalizado")
                    stats_custom = {
                        'media': np.mean(st.session_state['numeros']),
                        'varianza': np.var(st.session_state['numeros'])
                    }
                    st.json(stats_custom)
                
                with col2:
                    st.markdown("#### Estadísticas numpy.random")
                    stats_np = {
                        'media': np.mean(st.session_state['numpy_nums']),
                        'varianza': np.var(st.session_state['numpy_nums'])
                    }
                    st.json(stats_np)


if __name__ == "__main__":
    main()
