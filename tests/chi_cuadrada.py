import numpy as np
from scipy import stats
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class ChiCuadrada:
    """
    Prueba Chi-Cuadrada para uniformidad
    
    Compara las frecuencias observadas en cada intervalo
    con las frecuencias esperadas bajo una distribución uniforme.
    
    Hipótesis:
    H0: Los números siguen una distribución uniforme
    H1: Los números no siguen una distribución uniforme
    
    Parámetros:
    -----------
    numeros : List[float]
        Lista de números aleatorios en [0, 1]
    nivel_significancia : float
        Nivel de significancia (default 0.05)
    num_intervalos : int, optional
        Número de intervalos (si es None, usa regla de Sturges)
    """
    
    numeros: List[float]
    nivel_significancia: float = 0.05
    num_intervalos: int = None
    
    def __post_init__(self):
        self._validar_datos()
        
    def _validar_datos(self):
        if not self.numeros:
            raise ValueError("La lista de números no puede estar vacía")
        if any(n < 0 or n > 1 for n in self.numeros):
            raise ValueError("Los números deben estar en el intervalo [0, 1]")
            
    def _calcular_intervalos(self) -> int:
        """Calcula el número óptimo de intervalos usando regla de Sturges"""
        n = len(self.numeros)
        if self.num_intervalos:
            return self.num_intervalos
        return int(np.ceil(1 + 3.322 * np.log10(n)))
    
    def ejecutar(self) -> Dict[str, Any]:
        """
        Ejecuta la prueba Chi-Cuadrada
        
        Retorna:
        --------
        dict : {
            'estadistico': float,
            'p_valor': float,
            'valor_critico': float,
            'gl': int,
            'frecuencias_observadas': List[int],
            'frecuencias_esperadas': List[float],
            'intervalos': List[Tuple[float, float]],
            'pasa': bool,
            'interpretacion': str
        }
        """
        n = len(self.numeros)
        k = self._calcular_intervalos()
        
        intervalos = np.linspace(0, 1, k + 1)
        frec_observadas, _ = np.histogram(self.numeros, bins=intervalos)
        frec_esperadas = np.full(k, n / k)
        
        estadistico = np.sum((frec_observadas - frec_esperadas) ** 2 / frec_esperadas)
        
        gl = k - 1
        valor_critico = stats.chi2.ppf(1 - self.nivel_significancia, gl)
        p_valor = 1 - stats.chi2.cdf(estadistico, gl)
        
        pasa = estadistico < valor_critico
        
        if pasa:
            interpretacion = (
                "✓ PASA: Los números son consistente con una distribución uniforme. "
                f"Chi² = {estadistico:.4f} < valor crítico = {valor_critico:.4f}"
            )
        else:
            interpretacion = (
                "✗ NO PASA: Los números NO son consistentes con una distribución uniforme. "
                f"Chi² = {estadistico:.4f} >= valor crítico = {valor_critico:.4f}"
            )
        
        return {
            'estadistico': round(estadistico, 6),
            'p_valor': round(p_valor, 6),
            'valor_critico': round(valor_critico, 6),
            'gl': gl,
            'frecuencias_observadas': frec_observadas.tolist(),
            'frecuencias_esperadas': frec_esperadas.tolist(),
            'intervalos': [(round(intervalos[i], 4), round(intervalos[i+1], 4)) 
                         for i in range(k)],
            'pasa': pasa,
            'interpretacion': interpretacion,
            'n': n,
            'k': k
        }
    
    def comparar_scipy(self) -> Dict[str, Any]:
        """
        Compara con la implementación de scipy.stats.chisquare
        
        Retorna:
        --------
        dict : Comparación de resultados
        """
        k = self._calcular_intervalos()
        intervalos = np.linspace(0, 1, k + 1)
        frec_observadas, _ = np.histogram(self.numeros, bins=intervalos)
        frec_esperadas = np.full(k, len(self.numeros) / k)
        
        result_scipy = stats.chisquare(frec_observadas, f_exp=frec_esperadas)
        
        propia = self.ejecutar()
        
        return {
            'propia': {
                'estadistico': propia['estadistico'],
                'p_valor': propia['p_valor']
            },
            'scipy': {
                'estadistico': round(result_scipy.statistic, 6),
                'p_valor': round(result_scipy.pvalue, 6)
            },
            'diferencia': {
                'estadistico': abs(propia['estadistico'] - result_scipy.statistic),
                'p_valor': abs(propia['p_valor'] - result_scipy.pvalue)
            },
            'conclusion': "Implementaciones coinciden" if abs(propia['estadistico'] - result_scipy.statistic) < 0.001 else "Diferencias encontradas"
        }
    
    def __str__(self):
        return f"Chi-Cuadrada(n={len(self.numeros)}, α={self.nivel_significancia})"
