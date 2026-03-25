# Simulador de Generadores de Números Aleatorios

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-orange)

Aplicación web interactiva para simular y analizar generadores de números pseudoaleatorios, con pruebas estadísticas y visualizaciones dinámicas.

## Características

### Generadores Implementados

| Generador | Descripción | Parámetros |
|-----------|-------------|-------------|
| **Congruencial Lineal** | X(n+1) = (a·X(n) + c) mod m | semilla, a, c, m, n, precisión |
| **Congruencial Multiplicativo** | X(n+1) = (a·X(n)) mod m | semilla, a, m, n, precisión |
| **Cuadrados Medios** | Método de cuadrados medios | semilla, k, truncamiento, n |

### Pruebas Estadísticas

| Prueba | Descripción | Comparación |
|--------|-------------|-------------|
| **Chi-Cuadrada** | Frecuencias observadas vs esperadas | ✅ vs scipy.stats.chisquare |
| **Poker** | Patrones de dígitos (4-5 dígitos) | ✅ Comparación manual |
| **Kolmogorov-Smirnov** | Función de distribución acumulada | ✅ vs scipy.stats.kstest |

### Visualizaciones

- 📊 Histograma interactivo
- 📈 Función de Distribución Empírica (ECDF)
- 🔮 Gráfico Q-Q
- 🔗 Gráfico de Correlación (Xi vs Xi+1)
- 🎲 Frecuencia de Dígitos
- 🎬 Histograma Animado
- 🔬 Comparación con numpy.random

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/random-numbers-simulator.git
cd random-numbers-simulator

# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## Uso

1. **Seleccionar Generador**: Elige Congruencial Lineal, Multiplicativo o Cuadrados Medios
2. **Configurar Parámetros**: Ajusta semilla, multiplicador, módulo, etc.
3. **Generar**: Haz clic en "Generar Números"
4. **Analizar**: Explora las pestañas de datos, visualizaciones y pruebas
5. **Comparar**: Compara con numpy.random

## Estructura del Proyecto

```
random-numbers-generator/
├── app.py                      # Aplicación Streamlit principal
├── requirements.txt            # Dependencias
├── config/
│   └── settings.py            # Configuraciones globales
├── generators/
│   ├── __init__.py
│   ├── congruencial_lineal.py
│   ├── congruencial_multiplicativo.py
│   └── cuadrados_medios.py
├── tests/
│   ├── __init__.py
│   ├── chi_cuadrada.py
│   ├── poker.py
│   └── kolmogorov_smirnov.py
├── visualization/
│   ├── __init__.py
│   ├── animated_charts.py
│   ├── comparison.py
│   └── interactive.py
└── README.md
```

## Ejemplo de Parámetros

### Congruencial Lineal (MINSTD)
- Semilla: 12345
- a: 16807
- c: 0
- m: 2147483647
- Precisión: 7

### Congruencial Multiplicativo
- Semilla: 12345
- a: 16807
- m: 2147483647

### Cuadrados Medios
- Semilla: 1234
- k: 4
- Truncamiento: 2k

## Tecnologías

- **Streamlit**: Interfaz web interactiva
- **Plotly**: Gráficos animados e interactivos
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas
- **SciPy**: Pruebas estadísticas de referencia

## Licencia

MIT License -自由 使用
