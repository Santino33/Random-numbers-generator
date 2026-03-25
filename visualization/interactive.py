import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict, Any, Optional


class InteractiveCharts:
    """
    Gráficos interactivos avanzados para análisis de números aleatorios
    """
    
    @staticmethod
    def create_histogram(numeros: List[float],
                        num_bins: int = None,
                        title: str = "Histograma de Frecuencias") -> go.Figure:
        """
        Crea un histograma interactivo con opciones de zoom
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        num_bins : int, optional
            Número de bins (si es None, usa Sturges)
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        n = len(numeros)
        if num_bins is None:
            num_bins = int(np.ceil(1 + 3.322 * np.log10(n)))
        
        fig = px.histogram(
            numeros, 
            nbins=num_bins,
            range_x=[0, 1],
            title=title,
            labels={'value': 'Valor (Ri)', 'count': 'Frecuencia'},
            color_discrete_sequence=['#2E86AB']
        )
        
        expected = n / num_bins
        fig.add_hline(
            y=expected, 
            line_dash="dash", 
            line_color="#DC3545",
            annotation_text=f"Esperado: {expected:.1f}",
            annotation_position="top right"
        )
        
        fig.update_layout(
            template="plotly_white",
            height=450,
            bargap=0.1,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_ecdf(numeros: List[float],
                   title: str = "Función de Distribución Empírica (ECDF)") -> go.Figure:
        """
        Crea un gráfico de función de distribución empírica
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        sorted_nums = np.sort(numeros)
        ecdf = np.arange(1, len(sorted_nums) + 1) / len(sorted_nums)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=sorted_nums,
            y=ecdf,
            mode='lines',
            name='ECDF',
            line=dict(color='#2E86AB', width=2)
        ))
        
        x_uniform = np.linspace(0, 1, 100)
        fig.add_trace(go.Scatter(
            x=x_uniform,
            y=x_uniform,
            mode='lines',
            name='Uniforme[0,1]',
            line=dict(color='#DC3545', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Valor (x)",
            yaxis_title="F(x)",
            xaxis_range=[-0.05, 1.05],
            yaxis_range=[-0.05, 1.05],
            template="plotly_white",
            height=450,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
        )
        
        return fig
    
    @staticmethod
    def create_qq_plot(numeros: List[float],
                      title: str = "Gráfico Q-Q") -> go.Figure:
        """
        Crea un gráfico Q-Q comparando con distribución uniforme
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        n = len(numeros)
        sorted_nums = np.sort(numeros)
        
        theoretical_quantiles = (np.arange(1, n + 1) - 0.5) / n
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=theoretical_quantiles,
            y=sorted_nums,
            mode='markers',
            name='Datos',
            marker=dict(color='#2E86AB', size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Línea identidad',
            line=dict(color='#DC3545', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Cuantiles teóricos (Uniforme)",
            yaxis_title="Cuantiles observados",
            xaxis_range=[-0.05, 1.05],
            yaxis_range=[-0.05, 1.05],
            template="plotly_white",
            height=450,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
        )
        
        return fig
    
    @staticmethod
    def create_box_plot(data_dict: Dict[str, List[float]],
                      title: str = "Diagrama de Caja") -> go.Figure:
        """
        Crea un diagrama de caja comparando múltiples generadores
        
        Parámetros:
        -----------
        data_dict : Dict[str, List[float]]
            Diccionario con {nombre: numeros}
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        fig = go.Figure()
        
        colors = ['#2E86AB', '#A23B72', '#28A745', '#DC3545', '#FFC107']
        
        for i, (name, numeros) in enumerate(data_dict.items()):
            fig.add_trace(go.Box(
                y=numeros,
                name=name,
                marker_color=colors[i % len(colors)],
                boxmean='sd'
            ))
        
        fig.update_layout(
            title=title,
            yaxis_title="Valor (Ri)",
            template="plotly_white",
            height=450,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_3d_scatter(numeros: List[float],
                         title: str = "Visualización 3D (Xi, Xi+1, Xi+2)") -> go.Figure:
        """
        Crea un scatter plot 3D de tripletas consecutivas
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        nums = np.array(numeros[:-2])
        nums_next1 = np.array(numeros[1:-1])
        nums_next2 = np.array(numeros[2:])
        
        fig = go.Figure(data=[go.Scatter3d(
            x=nums[:500],
            y=nums_next1[:500],
            z=nums_next2[:500],
            mode='markers',
            marker=dict(
                size=4,
                color=nums[:500],
                colorscale='Viridis',
                opacity=0.8
            ),
            text=[f'Xi: {x:.4f}<br>Xi+1: {y:.4f}<br>Xi+2: {z:.4f}' 
                  for x, y, z in zip(nums[:500], nums_next1[:500], nums_next2[:500])],
            hoverinfo='text'
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Xi',
                yaxis_title='Xi+1',
                zaxis_title='Xi+2',
                xaxis_range=[0, 1],
                yaxis_range=[0, 1],
                zaxis_range=[0, 1]
            ),
            template="plotly_white",
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_digit_frequency(numeros: List[float],
                               title: str = "Frecuencia de Dígitos") -> go.Figure:
        """
        Crea un gráfico de frecuencia de cada dígito (0-9)
        
        Parámetros:
        -----------
        numeros : List[float]
            Lista de números generados
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        conteo = {str(i): 0 for i in range(10)}
        
        for num in numeros:
            num_str = str(num).replace('.', '')
            for d in num_str:
                if d.isdigit():
                    conteo[d] = conteo.get(d, 0) + 1
        
        digitos = list(conteo.keys())
        frecuencias = list(conteo.values())
        
        expected = sum(frecuencias) / 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=digitos,
            y=frecuencias,
            marker_color='#2E86AB',
            text=frecuencias,
            textposition='outside'
        ))
        
        fig.add_hline(
            y=expected,
            line_dash="dash",
            line_color="#DC3545",
            annotation_text=f"Esperado: {expected:.1f}",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Dígito",
            yaxis_title="Frecuencia",
            template="plotly_white",
            height=450
        )
        
        return fig
