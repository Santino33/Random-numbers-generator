import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict, Any, Optional


class AnimatedCharts:
    """
    Gráficos animados para visualización de generación de números aleatorios
    """
    
    @staticmethod
    def create_histogram_animation(numeros: List[float], 
                                   num_frames: int = 20,
                                   title: str = "Histograma Animado") -> go.Figure:
        """
        Crea un histograma animado que muestra la evolución de la distribución
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        num_frames : int
            Número de frames para la animación
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly con animación
        """
        numeros_array = np.array(numeros)
        n = len(numeros)
        
        if n < num_frames:
            num_frames = n
            
        indices = np.linspace(1, n, num_frames, dtype=int)
        
        fig = go.Figure()
        
        k = int(np.ceil(1 + 3.322 * np.log10(n)))
        
        for i, idx in enumerate(indices):
            data = numeros_array[:idx]
            counts, bins = np.histogram(data, bins=k, range=(0, 1))
            
            fig.add_trace(go.Bar(
                x=[(bins[j] + bins[j+1])/2 for j in range(len(counts))],
                y=counts,
                name=f'Iteración {idx}',
                visible=False,
                marker_color='rgba(46, 134, 171, 0.7)',
                marker_line_color='rgba(46, 134, 171, 1)',
                marker_line_width=1
            ))
        
        fig.data[0].visible = True
        
        steps = []
        for i in range(len(fig.data)):
            step = dict(
                method="update",
                args=[{"visible": [j == i for j in range(len(fig.data))]}],
                label=str(indices[i])
            )
            steps.append(step)
        
        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Números generados: "},
            pad={"t": 50},
            steps=steps
        )]
        
        fig.update_layout(
            title=title,
            xaxis_title="Valor (Ri)",
            yaxis_title="Frecuencia",
            sliders=sliders,
            template="plotly_white",
            height=500,
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                y=1.15,
                buttons=[
                    dict(label="▶ Play",
                         method="animate",
                         args=[None, dict(frame=dict(duration=200, redraw=True),
                                        fromcurrent=True)]),
                    dict(label="⏸ Pause",
                         method="animate",
                         args=[[None], dict(frame=dict(duration=0, redraw=False),
                                           mode="immediate")])
                ]
            )]
        )
        
        return fig
    
    @staticmethod
    def create_scatter_animation(numeros: List[float],
                                title: str = "Gráfico de Dispersión Animado") -> go.Figure:
        """
        Crea un scatter plot animado que muestra pares (Xi, Xi+1)
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly con animación
        """
        numeros_array = np.array(numeros[:-1])
        numeros_sig = np.array(numeros[1:])
        
        n = len(numeros_array)
        num_frames = min(20, n)
        indices = np.linspace(1, n, num_frames, dtype=int)
        
        fig = go.Figure()
        
        for i, idx in enumerate(indices):
            fig.add_trace(go.Scatter(
                x=numeros_array[:idx],
                y=numeros_sig[:idx],
                mode='markers',
                name=f'Iteración {idx}',
                visible=False,
                marker=dict(
                    size=8,
                    color=numeros_array[:idx],
                    colorscale='Viridis',
                    showscale=False
                )
            ))
        
        fig.data[0].visible = True
        
        steps = []
        for i in range(len(fig.data)):
            step = dict(
                method="update",
                args=[{"visible": [j == i for j in range(len(fig.data))]}],
                label=str(indices[i])
            )
            steps.append(step)
        
        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Pares generados: "},
            pad={"t": 50},
            steps=steps
        )]
        
        fig.update_layout(
            title=title,
            xaxis_title="Xi",
            xaxis_range=[-0.05, 1.05],
            yaxis_title="Xi+1",
            yaxis_range=[-0.05, 1.05],
            sliders=sliders,
            template="plotly_white",
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_timeline_animation(numeros: List[float],
                                  title: str = "Línea de Tiempo Animada") -> go.Figure:
        """
        Crea un gráfico de línea temporal animado
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly con animación
        """
        numeros_array = np.array(numeros)
        indices = np.arange(len(numeros_array))
        
        n = len(numeros_array)
        num_frames = min(30, n)
        frame_indices = np.linspace(1, n, num_frames, dtype=int)
        
        fig = go.Figure()
        
        for i, idx in enumerate(frame_indices):
            fig.add_trace(go.Scatter(
                x=indices[:idx],
                y=numeros_array[:idx],
                mode='lines+markers',
                name=f'Iteración {idx}',
                visible=False,
                line=dict(color='#2E86AB', width=1),
                marker=dict(size=3, color=numeros_array[:idx], colorscale='Plasma')
            ))
        
        fig.data[0].visible = True
        
        steps = []
        for i in range(len(fig.data)):
            step = dict(
                method="update",
                args=[{"visible": [j == i for j in range(len(fig.data))]}],
                label=str(frame_indices[i])
            )
            steps.append(step)
        
        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Números: "},
            pad={"t": 50},
            steps=steps
        )]
        
        fig.update_layout(
            title=title,
            xaxis_title="Índice",
            yaxis_title="Valor (Ri)",
            yaxis_range=[-0.05, 1.05],
            sliders=sliders,
            template="plotly_white",
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_frequency_heatmap(numeros: List[float],
                                 digitos: int = 5,
                                 title: str = "Heatmap de Frecuencia de Dígitos") -> go.Figure:
        """
        Crea un heatmap mostrando la frecuencia de cada dígito por posición
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        digitos : int
            Número de dígitos a analizar
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        frecuencia = np.zeros((digitos, 10))
        
        for num in numeros:
            num_str = str(num).replace('.', '').zfill(digitos)[-digitos:]
            for pos, dig in enumerate(num_str):
                frecuencia[pos, int(dig)] += 1
        
        fig = go.Figure(data=go.Heatmap(
            z=frecuencia,
            x=[str(i) for i in range(10)],
            y=[f'Pos {i+1}' for i in range(digitos)],
            colorscale='Blues',
            showscale=True
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Dígito",
            yaxis_title="Posición",
            template="plotly_white",
            height=400
        )
        
        return fig
