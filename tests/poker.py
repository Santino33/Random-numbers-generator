import numpy as np
from scipy import stats
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class PruebaPoker:
    """
    Prueba Poker para aleatoriedad de dígitos
    
    Analiza grupos de 5 dígitos y clasifica según los patrones
    típicos del poker (todos diferentes, un par, dos pares, etc.)
    
    Para 5 dígitos:
    - Todos diferentes (ABCD): 30240/100000 = 0.3024
    - Un par (AABCD): 50400/100000 = 0.5040
    - Dos pares (AABBC): 10800/100000 = 0.1080
    - Tres iguales (AAABC): 7200/100000 = 0.0720
    - Full house (AABBB): 900/100000 = 0.0090
    - Cuatro iguales (AAAAB): 450/100000 = 0.0045
    - Cinco iguales (AAAAA): 10/100000 = 0.0001
    
    Parámetros:
    -----------
    numeros : List[float]
        Lista de números aleatorios en [0, 1]
    nivel_significancia : float
        Nivel de significancia (default 0.05)
    digitos : int
        Número de dígitos por grupo (default 5)
    """
    
    numeros: List[float]
    nivel_significancia: float = 0.05
    digitos: int = 5
    
    def __post_init__(self):
        self._validar_datos()
        self._cargar_probabilidades()
        
    def _validar_datos(self):
        if not self.numeros:
            raise ValueError("La lista de números no puede estar vacía")
        if len(self.numeros) < self.digitos:
            raise ValueError(f"Se necesitan al menos {self.digitos} números")
            
    def _cargar_probabilidades(self):
        """Carga las probabilidades teóricas según el número de dígitos"""
        if self.digitos == 5:
            self.probabilidades = {
                'todos_diferentes': 0.3024,
                'un_par': 0.5040,
                'dos_pares': 0.1080,
                'tres_iguales': 0.0720,
                'full_house': 0.0090,
                'cuatro_iguales': 0.0045,
                'cinco_iguales': 0.0001
            }
            self.categorias = 7
        elif self.digitos == 4:
            self.probabilidades = {
                'todos_diferentes': 0.5040,
                'un_par': 0.4320,
                'dos_pares': 0.0270,
                'tres_iguales': 0.0360,
                'cuatro_iguales': 0.0010
            }
            self.categorias = 5
        else:
            raise ValueError(f"Dígitos {self.digitos} no soportados. Use 4 o 5")
    
    def _obtener_digitos(self, numero: float) -> List[int]:
        """Convierte un número en lista de dígitos"""
        num_str = str(numero).replace('.', '')[-self.digitos:]
        return [int(d) for d in num_str.zfill(self.digitos)]
    
    def _clasificar_mano(self, digitos: List[int]) -> str:
        """Clasifica una mano según el patrón de dígitos"""
        conteo = {}
        for d in digitos:
            conteo[d] = conteo.get(d, 0) + 1
        
        valores = sorted(conteo.values(), reverse=True)
        
        if self.digitos == 5:
            if valores == [5]:
                return 'cinco_iguales'
            elif valores == [4, 1]:
                return 'cuatro_iguales'
            elif valores == [3, 2]:
                return 'full_house'
            elif valores == [3, 1, 1]:
                return 'tres_iguales'
            elif valores == [2, 2, 1]:
                return 'dos_pares'
            elif valores == [2, 1, 1, 1]:
                return 'un_par'
            else:
                return 'todos_diferentes'
        elif self.digitos == 4:
            if valores == [4]:
                return 'cuatro_iguales'
            elif valores == [3, 1]:
                return 'tres_iguales'
            elif valores == [2, 2]:
                return 'dos_pares'
            elif valores == [2, 1, 1]:
                return 'un_par'
            else:
                return 'todos_diferentes'
    
    def ejecutar(self) -> Dict[str, Any]:
        """
        Ejecuta la prueba Poker
        
        Retorna:
        --------
        dict : {
            'estadistico': float,
            'p_valor': float,
            'valor_critico': float,
            'gl': int,
            'frecuencias_observadas': Dict[str, int],
            'frecuencias_esperadas': Dict[str, float],
            'pasa': bool,
            'interpretacion': str
        }
        """
        n = len(self.numeros)
        num_grupos = n // self.digitos
        
        conteo_observado = {cat: 0 for cat in self.probabilidades.keys()}
        
        for i in range(num_grupos):
            grupo = self.numeros[i * self.digitos:(i + 1) * self.digitos]
            digitos = []
            for num in grupo:
                digitos.extend(self._obtener_digitos(num))
            
            if len(digitos) >= self.digitos:
                digitos = digitos[:self.digitos]
                categoria = self._clasificar_mano(digitos)
                conteo_observado[categoria] += 1
        
        frec_observadas = np.array(list(conteo_observado.values()))
        frec_esperadas = np.array(list(self.probabilidades.values())) * num_grupos
        
        frec_esperadas = np.maximum(frec_esperadas, 5)
        
        estadistico = np.sum((frec_observadas - frec_esperadas) ** 2 / frec_esperadas)
        
        gl = self.categorias - 1
        valor_critico = stats.chi2.ppf(1 - self.nivel_significancia, gl)
        p_valor = 1 - stats.chi2.cdf(estadistico, gl)
        
        pasa = estadistico < valor_critico
        
        if pasa:
            interpretacion = (
                "✓ PASA: La secuencia pasa la prueba Poker. "
                f"Chi² = {estadistico:.4f} < valor crítico = {valor_critico:.4f}"
            )
        else:
            interpretacion = (
                "✗ NO PASA: La secuencia NO pasa la prueba Poker. "
                f"Chi² = {estadistico:.4f} >= valor crítico = {valor_critico:.4f}"
            )
        
        return {
            'estadistico': round(estadistico, 6),
            'p_valor': round(p_valor, 6),
            'valor_critico': round(valor_critico, 6),
            'gl': gl,
            'frecuencias_observadas': conteo_observado,
            'frecuencias_esperadas': {k: round(v * num_grupos, 2) for k, v in self.probabilidades.items()},
            'pasa': pasa,
            'interpretacion': interpretacion,
            'n': n,
            'num_grupos': num_grupos,
            'digitos': self.digitos
        }
    
    def __str__(self):
        return f"Prueba Poker(n={len(self.numeros)}, digitos={self.digitos})"
