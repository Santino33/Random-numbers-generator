import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class CuadradosMedios:
    """
    Generador de Números Aleatorios - Cuadrados Medios (Middle Squares)
    
    Algoritmo:
    1. X0 = semilla (k dígitos)
    2. Xi+1 = (Xi)^2
    3. Tomar los k dígitos centrales de Xi+1
    4. Ri = Xi / (10^k - 1)
    
    Parámetros:
    -----------
    semilla : int
        Valor inicial X(0)
    k : int
        Cantidad de dígitos a utilizar (2-10)
    n : int
        Cantidad de números a generar
    truncamiento : str
        '2k' = tomar 2k dígitos centrales
        'k' = tomar k dígitos centrales
    """
    
    semilla: int
    k: int = 4
    n: int = 100
    truncamiento: str = '2k'
    
    def __post_init__(self):
        self._validar_parametros()
        self._secuencia: List[int] = []
        self._numeros: List[float] = []
        self._periodo: Optional[int] = None
        self._historial: List[Tuple[int, int, float]] = []
        
    def _validar_parametros(self):
        if self.k < 2 or self.k > 10:
            raise ValueError("El parámetro k debe estar entre 2 y 10")
        if self.truncamiento not in ['2k', 'k']:
            raise ValueError("El truncamiento debe ser '2k' o 'k'")
        if self.n <= 0:
            raise ValueError("La cantidad de números debe ser mayor que 0")
        if self.semilla < 0:
            raise ValueError("La semilla debe ser no negativa")
            
        max_seed = 10**self.k - 1
        if self.semilla > max_seed:
            raise ValueError(f"La semilla no puede tener más de {self.k} dígitos")
        if self.semilla == 0 and self.truncamiento == 'k':
            raise ValueError("No se puede usar semilla 0 con truncamiento 'k'")
            
    def _obtener_digitos_centrales(self, numero: int) -> int:
        """Obtiene los dígitos centrales del número"""
        numero_str = str(numero).zfill(2 * self.k)
        
        if self.truncamiento == '2k':
            inicio = (len(numero_str) - 2 * self.k) // 2
            fin = inicio + 2 * self.k
        else:
            inicio = (len(numero_str) - self.k) // 2
            fin = inicio + self.k
            
        digitos = numero_str[inicio:fin]
        return int(digitos) if digitos else 0
    
    def generar(self) -> List[float]:
        """Genera la secuencia completa de números aleatorios"""
        self._secuencia = []
        self._numeros = []
        self._historial = []
        
        xi = self.semilla
        divisor = 10 ** self.k - 1
        
        seen = {}
        
        for i in range(self.n):
            xi_cuadrado = xi ** 2
            xi = self._obtener_digitos_centrales(xi_cuadrado)
            ri = round(xi / divisor, self.k)
            
            self._secuencia.append(xi)
            self._numeros.append(ri)
            self._historial.append((xi_cuadrado, xi, ri))
            
            if xi in seen and self._periodo is None:
                self._periodo = i - seen[xi]
            seen[xi] = i
                
        return self._numeros
    
    def generar_iterativo(self):
        """Generador iterativo para animaciones"""
        xi = self.semilla
        divisor = 10 ** self.k - 1
        
        seen = {}
        
        for i in range(self.n):
            xi_cuadrado = xi ** 2
            xi = self._obtener_digitos_centrales(xi_cuadrado)
            ri = round(xi / divisor, self.k)
            
            if xi in seen and self._periodo is None:
                self._periodo = i - seen[xi]
            seen[xi] = i
            
            yield i, xi_cuadrado, xi, ri
    
    @property
    def secuencia(self) -> List[int]:
        return self._secuencia
    
    @property
    def numeros(self) -> List[float]:
        return self._numeros
    
    @property
    def periodo(self) -> Optional[int]:
        return self._periodo
    
    @property
    def historial(self) -> List[Tuple[int, int, float]]:
        return self._historial
    
    def get_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas básicas de la secuencia"""
        if not self._numeros:
            self.generar()
        return {
            'media': np.mean(self._numeros),
            'varianza': np.var(self._numeros),
            'desviacion': np.std(self._numeros),
            'min': min(self._numeros),
            'max': max(self._numeros),
            'periodo': self._periodo,
            'n': len(self._numeros),
            'parametros': {
                'semilla': self.semilla,
                'k': self.k,
                'truncamiento': self.truncamiento
            }
        }
    
    def __str__(self):
        return f"Cuadrados Medios(k={self.k}, truncamiento={self.truncamiento}, n={self.n})"
    
    def __repr__(self):
        return self.__str__()
