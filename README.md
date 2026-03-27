# Simulador de Generadores de Números Aleatorios

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-orange)

Aplicación web interactiva para simular y analizar generadores de números pseudoaleatorios, con pruebas estadísticas y visualizaciones dinámicas.

## Arquitectura y Documentación del Sistema (Modelo C4)

A continuación se presenta la arquitectura definida bajo el modelo C4 (Nivel 2: Diagrama de Contenedores), destacando cómo interactúan las piezas de software para entregar el simulador matemático:

![Arquitectura C4 de la Aplicación](C:\Users\david\.gemini\antigravity\brain\4e2bfdca-1a49-4d12-b389-36fe918164fc\c4_architecture_diagram_1774584462238.png)

La aplicación sigue una arquitectura limpia orientada a componentes modulares con las siguientes capas y responsabilidades:

### 1. Sistema Frontend / Orquestador (`app.py`)
Actúa como la aplicación web central expuesta al usuario (vía *Streamlit*). Se encarga de manejar los estados de sesión de navegación, solicitar las configuraciones del usuario (ejemplo: semilla $X_0$, multiplicador $a$, incremento $c$, módulo $m$), inyectar los llamados a las rutinas matemáticas para evitar la re-evaluación indiscriminada y de coordinar el traspaso de variables ("payloads") entre los módulos subsecuentes.

### 2. Módulo de Generadores Matemáticos (`generators/`)
Este subsistema posee la responsabilidad estructural de albergar los algoritmos generadores de números pseudoaleatorios:
- **Congruencial Lineal**: Evalúa las semillas mediante un sistema polinomial modular: $X_{n+1} = (aX_n + c) \pmod m$. 
- **Congruencial Multiplicativo**: Opera bajo el factor de un congruencial recursivo donde $c=0$: $X_{n+1} = (aX_n) \pmod m$. Suele estar optimizado frente a bases binarias paritarias.
- **Cuadrados Medios**: Desarrolla la técnica clásica de Von Neumann utilizando la variable semilla iterativa al cuadrado sobre $k$ dígitos, y se extraen cíclicamente sus tramos céntricos.

### 3. Motor Estadístico de Pruebas (`tests/`)
Responsable de someter secuencias artificiales pseudoaleatorias a escrutinio para garantizar su Uniformidad e Independencia:
- **Prueba Chi-Cuadrada**: Segmenta y clasifica el intervalo total (0, 1) en subintervalos. Evalúa la desviación empírica de sus frecuencias de grupo frente a los coeficientes perfectos uniformemente esperados ($E_i$). Usando grados de libertad, se aprueba solo si el margen diferencial es menor al límite porcentual de la significancia teórica $\alpha$.
- **Prueba Póker**: Trabaja la independencia intrínseca analizando arreglos consecutivos de 5 dígitos o cifras, evaluando frecuencias relativas análogas al mazo de cartas de póker clásico ('Full House', 'Par', 'Quintilla'). Sirve para evidenciar sesgos de asociación grupal microscópicos y predecibilidad.
- **Kolmogorov-Smirnov (KS)**: Inspecciona toda la cadena iterativa acumulada $F_n(x)$ graficándola sobre una uniformidad pura $F(x)$ para denotar el error de diferencia local máxima absoluto $D$. No sufre de la estigmatización discreta al carecer de celdas divisorias.

### 4. Motor de Diagnóstico Visual (`visualization/`)
Transforma resultados abstractos crudos en modelos representacionales accionables usando `Plotly`:
- **Histogramas e Histogramas Animados**: Otorgan una validación instantánea del equilibrio topográfico; la serie debe de ser preferentemente plana para aprobar la distribución estocástica uniforme.
- **Rutas de Distribución (ECDF y Quantiles Q-Q)**: Ilustran a gran escala la adherencia ideal en matrices empíricas. Evalúan qué tanto concuerda visualmente la subida del volumen en comparación a una ascendencia de función perfecta paralela y continua.
- **Dispersión Lag / Correlación ($X_i$ vs $X_{i+1}$)**: Visualiza la dependencia transicional en 2D arrojando puntos encadenados iterativamente. Evidencia formaciones "cristalinas, rayas o fractales" en generadores que sufren de ciclismos de muy bajo orden que demuestran una total incapacidad de generar verdadera entropía estocástica.
- **Frecuencias Posicionales por Dígito**: Desintegra las respuestas de decimales en contadores base para auditar de forma rudimentaria favoritismos de mantisas lógicas en hardware (como sobredosis de '0's' en el generador Cuadrado Medio).

---

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
