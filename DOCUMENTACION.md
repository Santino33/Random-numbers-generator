# 📖 Documentación del Simulador de Números Aleatorios

## 1. Introducción

Este proyecto es un simulador interactivo de generadores de números pseudoaleatorios que incluye tres métodos de generación y tres pruebas estadísticas para validar la calidad de los números generados. La aplicación permite visualizar los resultados de manera dinámica y compararlos con funciones de bibliotecas estándar de Python.

---

## 2. Generadores de Números Aleatorios

### 2.1 Congruencial Lineal (LCG)

El generador congruencial lineal es uno de los métodos más clásicos y utilizados para generar secuencias de números pseudoaleatorios.

**Fórmula matemática:**
```
X(n+1) = (a × X(n) + c) mod m
R(n) = X(n) / m
```

**Parámetros:**

| Parámetro | Descripción | Efecto en la generación |
|-----------|-------------|-------------------------|
| **Semilla (X₀)** | Valor inicial de la secuencia | Determina el punto de partida. La misma semilla producirá la misma secuencia de números. |
| **Multiplicador (a)** | Constante que multiplica el valor anterior | Afecta el período de la secuencia. Un buen multiplicador produce períodos más largos. |
| **Incremento (c)** | Constante que se suma al producto | Cuando c=0, se llama "multiplicativo puro". Afecta la distribución de los números. |
| **Módulo (m)** | Límite superior del espacio de estados | Define el rango de valores posibles [0, m-1]. Debe ser grande para mayor período. |
| **Precisión** | Número de decimales en Ri | Determina la resolución de los números generados (típicamente 7 decimales). |
| **Cantidad (n)** | Cantidad de números a generar | Define cuántos números se producirán en la secuencia. |

**Recomendaciones de parámetros:**
- Para período completo: m debe ser potencia de 2, c debe ser divisible por 4
- Un buen multiplicador: a = 16807 (MINSTD)
- Módulo recomendado: m = 2,147,483,647 (primo)

---

### 2.2 Congruencial Multiplicativo

Es una variante del congruencial lineal donde el incremento (c) es igual a 0.

**Fórmula matemática:**
```
X(n+1) = (a × X(n)) mod m
R(n) = X(n) / m
```

**Parámetros:**

| Parámetro | Descripción | Efecto en la generación |
|-----------|-------------|-------------------------|
| **Semilla (X₀)** | Valor inicial (debe ser impar para período completo) | Con semilla impar se logra período máximo. |
| **Multiplicador (a)** | Constante multiplicadora | Debe ser un número impar y menor que m. |
| **Módulo (m)** | Límite superior | Generalmente m = 2^k - 1 para período completo. |
| **Precisión** | Número de decimales | Determina la resolución de Ri. |
| **Cantidad (n)** | Cantidad de números | Cantidad a generar. |

**Nota importante:** Para lograr el período máximo posible, la semilla debe ser un número impar y el multiplicador debe ser una raíz primitiva del módulo.

---

### 2.3 Cuadrados Medios (Middle Squares)

Uno de los métodos más antiguos, propuesto por John von Neumann en 1946.

**Algoritmo:**
1. X₀ = semilla (con k dígitos)
2. Xi+1 = (Xi)²
3. Tomar los k dígitos centrales de Xi+1
4. Ri = Xi / (10^k - 1)

**Parámetros:**

| Parámetro | Descripción | Efecto en la generación |
|-----------|-------------|-------------------------|
| **Semilla (X₀)** | Valor inicial con k dígitos | Debe tener exactamente k dígitos. |
| **Dígitos (k)** | Cantidad de dígitos a utilizar (2-10) | Define el tamaño del espacio de búsqueda. k=4 es común. |
| **Truncamiento** | '2k' o 'k' | Define cuántos dígitos tomar del número cuadrado: 2k toma más dígitos, k toma menos. |
| **Cantidad (n)** | Cantidad de números | Cantidad a generar. |

**Advertencia:** El método de cuadrados medios tiene un período corto y puede degenerar rápidamente hacia cero si la semilla no es adecuada.

---

## 3. Visualizaciones

### 3.1 Histograma

**¿Qué muestra?**
Distribución de frecuencia de los números generados en intervalos iguales.

**¿Para qué sirve?**
- Visualizar si los números están distribuidos uniformemente
- Detectar sesgos o concentraciones anormales
- Comparar con la distribución esperada (línea horizontal punteada)

**Interpretación:**
- En una distribución uniforme ideal, todas las barras deben tener aproximadamente la misma altura
- Si hay barras mucho más altas o bajas, indica posibles patrones no aleatorios

---

### 3.2 Función de Distribución Empírica (ECDF)

**¿Qué muestra?**
La proporción de números menores o iguales a cada valor, comparada con la distribución teórica uniforme.

**¿Para qué sirve?**
- Compara visualmente la distribución acumulada de los datos con la línea diagonal (uniforme perfecta)
- La línea punteada roja representa la distribución teórica U[0,1]
- La línea azul es la distribución real de los números generados

**Interpretación:**
- Si la línea azul está cerca de la diagonal, los números son uniformes
- Desviaciones grandes indican falta de uniformidad

---

### 3.3 Gráfico Q-Q (Quantile-Quantile)

**¿Qué muestra?**
Compara los cuantiles de los datos generados con los cuantiles teóricos de una distribución uniforme.

**¿Para qué sirve?**
- Detectar desviaciones de la distribución uniforme
- Identificar valores atípicos
- Verificar visualmente si los datos siguen la distribución esperada

**Interpretación:**
- Los puntos deben seguir aproximadamente la línea diagonal
- Puntos alejados de la línea indican anomalías

---

### 3.4 Gráfico de Correlación (Xi vs Xi+1)

**¿Qué muestra?**
Diagrama de dispersión donde cada punto representa un par de números consecutivos (Xi, Xi+1).

**¿Para qué sirve?**
- Detectar correlaciones entre números consecutivos
- Identificar patrones estructurados
- Evaluar la independencia de los números

**Interpretación:**
- Los puntos deben distribuirse uniformemente en el cuadrado [0,1]×[0,1]
- Patrones lineales o clustering indican correlación (malo para aleatoriedad)
- El coeficiente de correlación (r) debe ser cercano a 0

---

### 3.5 Frecuencia de Dígitos

**¿Qué muestra?**
Conteo de cuántas veces aparece cada dígito (0-9) en todos los números generados.

**¿Para qué sirve?**
- Verificar que cada dígito aparezca aproximadamente el mismo número de veces
- Detectar sesgos en dígitos específicos

**Interpretación:**
- En una secuencia aleatoria perfecta, cada dígito debe aparecer ~10% de las veces
- La línea punteada roja indica la frecuencia esperada

---

### 3.6 Histograma Animado

**¿Qué muestra?**
Evolución del histograma a medida que se generan más números.

**¿Para qué sirve?**
- Visualizar cómo converge la distribución a medida que aumenta n
- Entender el comportamiento del generador en tiempo real

**Cómo usarlo:**
- Usa el slider para ver diferentes etapas de la generación
- Usa los botones Play/Pause para la animación automática

---

## 4. Pruebas Estadísticas

### 4.1 Prueba Chi-Cuadrada (χ²)

**¿Qué hace?**
Compara las frecuencias observadas en cada intervalo con las frecuencias esperadas bajo una distribución uniforme.

**Fórmula:**
```
χ² = Σ (Oi - Ei)² / Ei
```
Donde Oi = frecuencia observada y Ei = frecuencia esperada.

**¿Para qué sirve?**
- Determinar si los números siguen una distribución uniforme
- Detectar sesgos en la distribución

**Cómo se interpreta:**
- Se divide el intervalo [0,1] en k subintervalos (regla de Sturges: k = 1 + 3.322×log₁₀(n))
- Se cuenta cuántos números caen en cada intervalo
- Se compara con la frecuencia esperada (n/k)
- Si χ² < valor crítico → PASA (los números son uniformes)
- Si χ² ≥ valor crítico → NO PASA (los números no son uniformes)

**Nivel de significancia (α):**
- α = 0.05 significa 5% de probabilidad de rechazar correctamente
- Valores típicos: 0.01, 0.05, 0.10

---

### 4.2 Prueba Poker

**¿Qué hace?**
Analiza grupos de dígitos (típicamente 5) y los clasifica según patrones similares a las manos del poker.

**Categorías (para 5 dígitos):**
| Categoría | Ejemplo | Probabilidad teórica |
|-----------|---------|---------------------|
| Todos diferentes | 12345 | 0.3024 |
| Un par | 11234 | 0.5040 |
| Dos pares | 11223 | 0.1080 |
| Tres iguales | 11123 | 0.0720 |
| Full house | 11122 | 0.0090 |
| Cuatro iguales | 11112 | 0.0045 |
| Cinco iguales | 11111 | 0.0001 |

**¿Para qué sirve?**
- Detectar patrones en la distribución de dígitos
- Verificar que no haya repetición excesiva o insuficiente de dígitos

**Cómo se interpreta:**
- Se agrupan los dígitos de los números en grupos de 5
- Se clasifica cada grupo en una categoría
- Se comparan las frecuencias observadas con las esperadas
- Si χ² < valor crítico → PASA

---

### 4.3 Prueba Kolmogorov-Smirnov (K-S)

**¿Qué hace?**
Compara la función de distribución empírica (EDF) con la función de distribución teórica de una uniforme[0,1].

**Fórmulas:**
```
D+ = max(i/n - F(xi))
D- = max(F(xi) - (i-1)/n)
D = max(D+, D-)
```

Donde F(xi) es el valor teórico (xi para uniforme) y n es el tamaño de muestra.

**¿Para qué sirve?**
- Prueba de bondad de ajuste más precisa que chi-cuadrada
- Funciona bien para datos continuos

**Cómo se interpreta:**
- Calcula la máxima desviación entre la distribución acumulativa observada y la teórica
- Si D < valor crítico → PASA (los números siguen la distribución uniforme)
- Es más sensible a diferencias cerca del centro de la distribución

---

### Diferencias entre las tres pruebas

| Característica | Chi-Cuadrada | Poker | K-S |
|----------------|--------------|-------|-----|
| **Enfoque** | Frecuencias por intervalos | Patrones de dígitos | Distribución acumulativa |
| **Mejor para** | Datos discretizados | Análisis de dígitos | Datos continuos |
| **Sensibilidad** | A toda la distribución | A patrones repetitivos | A desviaciones locales |
| **Categorías** | k intervalos | 7 categorías (5 dígitos) | Comparación continua |

---

## 5. Comparación con Bibliotecas

### 5.1 ¿Por qué comparar?

Permite evaluar si los generadores implementados son comparables en calidad con los generadores estándar de Python.

### 5.2 Bibliotecas comparadas

1. **numpy.random**: Generador Mersenne Twister (estándar de facto en Python)
2. **scipy.stats**: Funciones estadísticas de referencia

### 5.3 Gráficos de comparación

**Histograma Comparativo:**
- Compara visualmente la distribución de frecuencias entre el generador personalizado y numpy.random
- Ambos histogramas deben ser similares si el generador es bueno

**ECDF Comparativo:**
- Compara las funciones de distribución acumulativa
- Las líneas deben coincidir aproximadamente con la diagonal teórica

### 5.4 Métricas comparadas

| Métrica | Descripción | Valor ideal (Uniforme) |
|---------|-------------|----------------------|
| **Media** | Promedio de todos los números | 0.5 |
| **Varianza** | Dispersión de los datos | 1/12 ≈ 0.083 |

**Interpretación:**
- Valores cercanos a los ideales indican buen comportamiento
- Diferencias grandes entre personalizado y numpy pueden indicar problemas

---

## 6. Uso de la Aplicación

### 6.1 Flujo de trabajo típico

1. **Seleccionar generador** desde el sidebar
2. **Configurar parámetros** según el tipo de generador
3. **Generar números** con el botón "Generar Números"
4. **Explorar datos** en la pestaña "Datos"
5. **Visualizar** en la pestaña "Visualización"
6. **Ejecutar pruebas** en la pestaña "Pruebas"
7. **Comparar** con numpy en la pestaña "Comparación"

### 6.2 Configuración de parámetros comunes

**Congruencial Lineal (recomendado):**
```
Semilla: 12345
a: 16807
c: 0
m: 2147483647
n: 1000
Precisión: 7
```

**Cuadrados Medios:**
```
Semilla: 1234
k: 4
Truncamiento: 2k
n: 100
```

### 6.3 Interpretación de resultados

- **PASA**: El generador pasó la prueba (los números son consistentes con aleatoriedad)
- **NO PASA**: El generador no pasó (posibles patrones o sesgos detectados)

**Nota:** Un "NO PASA" no significa necesariamente que el generador sea malo; puede necesitar más números o diferentes parámetros.

---

## 7. Autores y Referencias

Basado en metodologías de simulación y generación de números aleatorios descritas en:
- "Simulation and Modelling" - Geoffrey Gordon
- Documentación de scipy.stats
- NIST Statistical Test Suite

---

*Documentación generada automáticamente para el proyecto Simulador de Números Aleatorios*