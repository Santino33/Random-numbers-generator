import numpy as np
from scipy import stats
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class KolmogorovSmirnov:
    """
    Prueba Kolmogorov-Smirnov para uniformidad
    
    Compara la función de distribución empírica (EDF) de los datos
    con la función de distribución teórica de una uniforme[0,1].
    
    Hipótesis:
    H0: Los números siguen una distribución uniforme[0,1]
    H1: Los números no siguen una distribución uniforme[0,1]
    
    Parámetros:
    -----------
    numeros : List[float]
        Lista de números aleatorios en [0, 1]
    nivel_significancia : float
        Nivel de significancia (default 0.05)
    """
    
    numeros: List[float]
    nivel_significancia: float = 0.05
    
    def __post_init__(self):
        self._validar_datos()
        
    def _validar_datos(self):
        if not self.numeros:
            raise ValueError("La lista de números no puede estar vacía")
        if any(n < 0 or n > 1 for n in self.numeros):
            raise ValueError("Los números deben estar en el intervalo [0, 1]")
    
    def _calcular_d_plus(self, datos_ordenados: np.ndarray, n: int) -> float:
        """Calcula D+ = max(i/n - F(x_i))"""
        d_plus = 0
        for i, x in enumerate(datos_ordenados, 1):
            valor = (i / n) - x
            if valor > d_plus:
                d_plus = valor
        return d_plus
    
    def _calcular_d_minus(self, datos_ordenados: np.ndarray, n: int) -> float:
        """Calcula D- = max(F(x_i) - (i-1)/n)"""
        d_minus = 0
        for i, x in enumerate(datos_ordenados, 1):
            valor = x - ((i - 1) / n)
            if valor > d_minus:
                d_minus = valor
        return d_minus
    
    def ejecutar(self) -> Dict[str, Any]:
        """
        Ejecuta la prueba Kolmogorov-Smirnov
        
        Retorna:
        --------
        dict : {
            'estadistico': float,
            'valor_critico': float,
            'p_valor': float,
            'd_plus': float,
            'd_minus': float,
            'pasa': bool,
            'interpretacion': str,
            'datos_ordenados': List[float],
            'datos_ordenados': List[float]
        }
        """
        n = len(self.numeros)
        datos_ordenados = np.sort(self.numeros)
        
        d_plus = self._calcular_d_plus(datos_ordenados, n)
        d_minus = self._calcular_d_minus(datos_ordenados, n)
        
        estadistico = max(d_plus, d_minus)
        
        valor_critico = stats.kstwobign.ppf(1 - self.nivel_significancia) / np.sqrt(n)
        
        p_valor = 1 - stats.kstwobign.cdf(estadistico * np.sqrt(n))
        
        pasa = estadistico < valor_critico
        
        if pasa:
            interpretacion = (
                "✓ PASA: Los números son consistentes con distribución uniforme. "
                f"D = {estadistico:.4f} < valor crítico = {valor_critico:.4f}"
            )
        else:
            interpretacion = (
                "✗ NO PASA: Los números NO son consistentes con distribución uniforme. "
                f"D = {estadistico:.4f} >= valor crítico = {valor_critico:.4f}"
            )
        
        return {
            'estadistico': round(estadistico, 6),
            'valor_critico': round(valor_critico, 6),
            'p_valor': round(p_valor, 6),
            'd_plus': round(d_plus, 6),
            'd_minus': round(d_minus, 6),
            'pasa': pasa,
            'interpretacion': interpretacion,
            'n': n,
            'datos_ordenados': datos_ordenados.tolist()
        }
    
    def comparar_scipy(self) -> Dict[str, Any]:
        """
        Compara con la implementación de scipy.stats.kstest
        
        Retorna:
        --------
        dict : Comparación de resultados
        """
        result_scipy = stats.kstest(self.numeros, 'uniform')
        
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
            'conclusion': "Implementaciones coinciden" if abs(propia['estadistico'] - result_scipy.statistic) < 0.0001 else "Diferencias encontradas"
        }
    
    def __str__(self):
        return f"Kolmogorov-Smirnov(n={len(self.numeros)}, α={self.nivel_significancia})"
