import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class CongruencialMultiplicativo:
    """
    Generador de Números Aleatorios - Congruencial Multiplicativo
    
    Formula: X(n+1) = (a * X(n)) mod m
    Ri = Xi / m
    
    El multiplicador 'a' debe ser un número primo respecto a m
    y mayor que sqrt(m) para buen período.
    
    Parámetros:
    -----------
    semilla : int
        Valor inicial X(0)
    a : int
        Multiplicador (debe ser impar y menor que m)
    m : int
        Módulo (generalmente 2^k - 1 para período completo)
    n : int
        Cantidad de números a generar
    precision : int
        Cantidad de decimales para Ri
    """
    
    semilla: int
    a: int
    m: int
    n: int = 1000
    precision: int = 7
    
    def __post_init__(self):
        self._validar_parametros()
        self._secuencia: List[int] = []
        self._numeros: List[float] = []
        self._periodo: Optional[int] = None
        self._historial: List[Tuple[int, float]] = []
        
    def _validar_parametros(self):
        if self.m <= 0:
            raise ValueError("El módulo m debe ser mayor que 0")
        if self.a < 0:
            raise ValueError("El multiplicador a debe ser no negativo")
        if self.a >= self.m:
            raise ValueError(f"El multiplicador a={self.a} debe ser menor que m={self.m}")
        if self.semilla < 0 or self.semilla >= self.m:
            raise ValueError(f"La semilla debe estar en [0, {self.m-1}]")
        if self.n <= 0:
            raise ValueError("La cantidad de números debe ser mayor que 0")
        if self.semilla % 2 == 0 and self.semilla != 0:
            import warnings
            warnings.warn("Para período completo, la semilla debe ser impar", UserWarning)
            
    def generar(self) -> List[float]:
        """Genera la secuencia completa de números aleatorios"""
        self._secuencia = []
        self._numeros = []
        self._historial = []
        
        xi = self.semilla
        
        for i in range(self.n):
            xi = (self.a * xi) % self.m
            ri = round(xi / self.m, self.precision)
            
            self._secuencia.append(xi)
            self._numeros.append(ri)
            self._historial.append((xi, ri))
            
            if self._periodo is None and xi == self.semilla and i > 0:
                self._periodo = i
                
        return self._numeros
    
    def generar_iterativo(self):
        """Generador iterativo para animaciones"""
        xi = self.semilla
        for i in range(self.n):
            xi = (self.a * xi) % self.m
            ri = round(xi / self.m, self.precision)
            yield i, xi, ri
            
            if self._periodo is None and xi == self.semilla and i > 0:
                self._periodo = i
                
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
    def historial(self) -> List[Tuple[int, float]]:
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
                'a': self.a,
                'm': self.m,
                'precision': self.precision
            }
        }
    
    def __str__(self):
        return f"Congruencial Multiplicativo(a={self.a}, m={self.m}, n={self.n})"
    
    def __repr__(self):
        return self.__str__()
