import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict, Any, Optional


class ComparisonCharts:
    """
    Gráficos de comparación entre generadores y con bibliotecas estándar
    """
    
    @staticmethod
    def compare_histograms(data_list: List[tuple],
                          labels: List[str],
                          title: str = "Comparación de Histogramas") -> go.Figure:
        """
        Compara histogramas de múltiples generadores
        
        Parámetros:
        -----------
        data_list : List[tuple]
            Lista de tuplas (numeros, label)
        labels : List[str]
            Nombres de cada conjunto de datos
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        fig = make_subplots(rows=1, cols=len(data_list),
                          subplot_titles=labels)
        
        colors = ['#2E86AB', '#A23B72', '#28A745', '#DC3545', '#FFC107']
        
        for i, (numeros, label) in enumerate(data_list):
            numeros_array = np.array(numeros)
            k = int(np.ceil(1 + 3.322 * np.log10(len(numeros))))
            
            counts, bins = np.histogram(numeros_array, bins=k, range=(0, 1))
            x_vals = [(bins[j] + bins[j+1])/2 for j in range(len(counts))]
            
            fig.add_trace(
                go.Bar(x=x_vals, y=counts, name=label,
                      marker_color=colors[i % len(colors)],
                      showlegend=False),
                row=1, col=i+1
            )
        
        fig.update_layout(
            title=title,
            template="plotly_white",
            height=400,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def compare_with_libraries(numeros: List[float],
                               numpy_numbers: List[float],
                               title: str = "Comparación con Bibliotecas") -> go.Figure:
        """
        Compara la distribución del generador con numpy.random y random
        
        Parámetros:
        -----------
        numeros : List[float]
            Números del generador personalizado
        numpy_numbers : List[float]
            Números de numpy.random
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        fig = make_subplots(rows=2, cols=2,
                          subplot_titles=('Histograma Personalizado', 
                                         'Histograma numpy.random',
                                         'ECDF Personalizado',
                                         'ECDF numpy.random'))
        
        k = int(np.ceil(1 + 3.322 * np.log10(len(numeros))))
        
        counts1, bins1 = np.histogram(numeros, bins=k, range=(0, 1))
        x1 = [(bins1[j] + bins1[j+1])/2 for j in range(len(counts1))]
        
        counts2, bins2 = np.histogram(numpy_numbers, bins=k, range=(0, 1))
        x2 = [(bins2[j] + bins2[j+1])/2 for j in range(len(counts2))]
        
        fig.add_trace(go.Bar(x=x1, y=counts1, name='Personalizado',
                           marker_color='#2E86AB'), row=1, col=1)
        fig.add_trace(go.Bar(x=x2, y=counts2, name='numpy',
                           marker_color='#A23B72'), row=1, col=2)
        
        sorted_nums = np.sort(numeros)
        ecdf = np.arange(1, len(sorted_nums) + 1) / len(sorted_nums)
        fig.add_trace(go.Scatter(x=sorted_nums, y=ecdf, mode='lines',
                                name='ECDF Personalizado',
                                line=dict(color='#2E86AB')), row=2, col=1)
        
        sorted_numpy = np.sort(numpy_numbers)
        ecdf_np = np.arange(1, len(sorted_numpy) + 1) / len(sorted_numpy)
        fig.add_trace(go.Scatter(x=sorted_numpy, y=ecdf_np, mode='lines',
                                name='ECDF numpy',
                                line=dict(color='#A23B72')), row=2, col=2)
        
        fig.update_layout(
            title=title,
            template="plotly_white",
            height=600,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_correlation_plot(numeros: List[float],
                               title: str = "Gráfico de Correlación (Xi vs Xi+1)") -> go.Figure:
        """
        Crea un scatter plot de pares consecutivos para analizar correlación
        
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
        nums = np.array(numeros[:-1])
        nums_next = np.array(numeros[1:])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=nums,
            y=nums_next,
            mode='markers',
            marker=dict(
                size=6,
                color=nums,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Valor Xi")
            ),
            text=[f'Xi: {x:.4f}<br>Xi+1: {y:.4f}' for x, y in zip(nums, nums_next)],
            hoverinfo='text'
        ))
        
        fig.add_shape(type="line",
                     x0=0, y0=0, x1=1, y1=1,
                     line=dict(color="gray", width=1, dash="dash"))
        
        corr = np.corrcoef(nums, nums_next)[0, 1]
        
        fig.update_layout(
            title=f"{title}<br><sub>Correlación: {corr:.6f}</sub>",
            xaxis_title="Xi",
            yaxis_title="Xi+1",
            xaxis_range=[-0.05, 1.05],
            yaxis_range=[-0.05, 1.05],
            template="plotly_white",
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_statistics_comparison(stats_dict: Dict[str, Dict[str, float]],
                                     title: str = "Comparación de Estadísticas") -> go.Figure:
        """
        Compara estadísticas entre diferentes generadores
        
        Parámetros:
        -----------
        stats_dict : Dict[str, Dict[str, float]]
            Diccionario con {nombre: {estadistica: valor}}
        title : str
            Título del gráfico
            
        Retorna:
        --------
        go.Figure : Figura de Plotly
        """
        generadores = list(stats_dict.keys())
        metricias = list(stats_dict[generadores[0]].keys())
        
        fig = make_subplots(rows=1, cols=len(metricias),
                          subplot_titles=metricias)
        
        colors = ['#2E86AB', '#A23B72', '#28A745', '#DC3545', '#FFC107']
        
        for i, metrica in enumerate(metricias):
            valores = [stats_dict[g].get(metrica, 0) for g in generadores]
            
            fig.add_trace(
                go.Bar(x=generadores, y=valores, name=metrica,
                      marker_color=colors[i % len(colors)]),
                row=1, col=i+1
            )
        
        fig.update_layout(
            title=title,
            template="plotly_white",
            height=400,
            showlegend=True
        )
        
        return fig
