"""
可视化模块
负责光谱曲线绘制和相似度结果可视化
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Optional, Dict
import streamlit as st
from .utils import (
    SpectralData, SimilarityResult, SimilarityMethod, 
    PlotOptions, FilterSettings
)


class SpectrumVisualizer:
    """光谱可视化器"""
    
    def __init__(self):
        self.default_colors = px.colors.qualitative.Set1
        self.color_schemes = {
            'plotly': px.colors.qualitative.Plotly,
            'set1': px.colors.qualitative.Set1,
            'set2': px.colors.qualitative.Set2,
            'set3': px.colors.qualitative.Set3,
            'tab10': px.colors.qualitative.Tab10,
            'tab20': px.colors.qualitative.Tab20
        }
    
    def plot_spectra(self, spectra: List[SpectralData], 
                    options: Optional[PlotOptions] = None,
                    filter_settings: Optional[FilterSettings] = None) -> go.Figure:
        """
        绘制光谱曲线
        
        Args:
            spectra: 光谱数据列表
            options: 绘图选项
            filter_settings: 筛选设置
            
        Returns:
            Plotly图表对象
        """
        if not spectra:
            return go.Figure()
        
        # 使用默认选项
        if options is None:
            options = PlotOptions()
        
        # 应用筛选
        if filter_settings:
            spectra = self._apply_filters(spectra, filter_settings)
        
        # 创建图表
        fig = go.Figure()
        
        # 获取颜色方案
        colors = self.color_schemes.get(options.color_scheme, self.default_colors)
        
        # 绘制每条光谱
        for i, spectrum in enumerate(spectra):
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=spectrum.wavelengths,
                y=spectrum.absorbances,
                mode='lines',
                name=spectrum.experiment_id,
                line=dict(
                    color=color,
                    width=options.line_width
                ),
                opacity=options.opacity,
                hovertemplate=(
                    f'<b>{spectrum.experiment_id}</b><br>' +
                    '波长: %{x:.1f} nm<br>' +
                    '吸光度: %{y:.4f}<br>' +
                    '<extra></extra>'
                )
            ))
        
        # 设置图表布局
        fig.update_layout(
            title=options.title,
            xaxis_title=options.x_label,
            yaxis_title=options.y_label,
            showlegend=options.show_legend,
            hovermode='closest',
            template='plotly_white',
            height=600,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # 设置坐标轴
        fig.update_xaxes(
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=False
        )
        fig.update_yaxes(
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=False
        )
        
        return fig
    
    def plot_similarity_results(self, result: SimilarityResult, 
                               options: Optional[PlotOptions] = None) -> go.Figure:
        """
        绘制相似度分析结果
        
        Args:
            result: 相似度计算结果
            options: 绘图选项
            
        Returns:
            Plotly图表对象
        """
        if not result:
            return go.Figure()
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('SAM相似度分布', '余弦相似度分布', 
                          '皮尔逊相关系数分布', '算法对比'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # SAM相似度直方图
        fig.add_trace(
            go.Histogram(
                x=result.sam_scores,
                name='SAM',
                nbinsx=20,
                marker_color='blue',
                opacity=0.7
            ),
            row=1, col=1
        )
        
        # 余弦相似度直方图
        fig.add_trace(
            go.Histogram(
                x=result.cosine_scores,
                name='余弦相似度',
                nbinsx=20,
                marker_color='red',
                opacity=0.7
            ),
            row=1, col=2
        )
        
        # 皮尔逊相关系数直方图
        fig.add_trace(
            go.Histogram(
                x=result.pearson_scores,
                name='皮尔逊相关系数',
                nbinsx=20,
                marker_color='green',
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # 算法对比散点图
        fig.add_trace(
            go.Scatter(
                x=result.sam_scores,
                y=result.cosine_scores,
                mode='markers',
                name='SAM vs 余弦',
                marker=dict(
                    color=result.pearson_scores,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="皮尔逊相关系数")
                ),
                hovertemplate=(
                    '实验ID: %{text}<br>' +
                    'SAM: %{x:.3f}<br>' +
                    '余弦: %{y:.3f}<br>' +
                    '<extra></extra>'
                ),
                text=result.experiment_ids
            ),
            row=2, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title="相似度分析结果",
            showlegend=False,
            height=800,
            template='plotly_white'
        )
        
        # 更新坐标轴标签
        fig.update_xaxes(title_text="相似度值", row=1, col=1)
        fig.update_xaxes(title_text="相似度值", row=1, col=2)
        fig.update_xaxes(title_text="相关系数", row=2, col=1)
        fig.update_xaxes(title_text="SAM相似度", row=2, col=2)
        
        fig.update_yaxes(title_text="频次", row=1, col=1)
        fig.update_yaxes(title_text="频次", row=1, col=2)
        fig.update_yaxes(title_text="频次", row=2, col=1)
        fig.update_yaxes(title_text="余弦相似度", row=2, col=2)
        
        return fig
    
    def plot_algorithm_comparison(self, comparison: Dict) -> go.Figure:
        """
        绘制算法性能比较图
        
        Args:
            comparison: 算法比较结果
            
        Returns:
            Plotly图表对象
        """
        if not comparison or 'correlations' not in comparison:
            return go.Figure()
        
        # 创建算法性能对比图
        methods = ['sam', 'cosine', 'pearson']
        metrics = ['mean', 'std', 'min', 'max']
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('算法性能对比', '算法间相关性'),
            specs=[[{"type": "bar"}, {"type": "heatmap"}]]
        )
        
        # 性能对比柱状图
        for i, metric in enumerate(metrics):
            values = [comparison[method][metric] for method in methods]
            fig.add_trace(
                go.Bar(
                    name=metric.upper(),
                    x=[m.upper() for m in methods],
                    y=values,
                    text=[f'{v:.3f}' for v in values],
                    textposition='auto',
                    opacity=0.8
                ),
                row=1, col=1
            )
        
        # 相关性热力图
        correlations = comparison['correlations']
        corr_matrix = np.array([
            [1.0, correlations['sam_cosine'], correlations['sam_pearson']],
            [correlations['sam_cosine'], 1.0, correlations['cosine_pearson']],
            [correlations['sam_pearson'], correlations['cosine_pearson'], 1.0]
        ])
        
        fig.add_trace(
            go.Heatmap(
                z=corr_matrix,
                x=['SAM', '余弦', '皮尔逊'],
                y=['SAM', '余弦', '皮尔逊'],
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.round(3),
                texttemplate="%{text}",
                textfont={"size": 12},
                colorbar=dict(title="相关系数")
            ),
            row=1, col=2
        )
        
        # 更新布局
        fig.update_layout(
            title="算法性能比较",
            height=500,
            template='plotly_white',
            showlegend=True
        )
        
        return fig
    
    def plot_top_similar_spectra(self, spectra: List[SpectralData], 
                                result: SimilarityResult,
                                method: SimilarityMethod,
                                top_n: int = 5) -> go.Figure:
        """
        绘制最相似的光谱
        
        Args:
            spectra: 光谱数据列表
            result: 相似度计算结果
            method: 相似度方法
            top_n: 显示前n个最相似的光谱
            
        Returns:
            Plotly图表对象
        """
        if not spectra or not result:
            return go.Figure()
        
        # 获取最相似的光谱
        top_similar = result.get_top_similar(method, top_n)
        top_ids = [item[0] for item in top_similar]
        top_scores = [item[1] for item in top_similar]
        
        # 筛选对应的光谱数据
        top_spectra = [s for s in spectra if s.experiment_id in top_ids]
        
        # 创建图表
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        
        # 绘制最相似的光谱
        for i, (spectrum, score) in enumerate(zip(top_spectra, top_scores)):
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=spectrum.wavelengths,
                y=spectrum.absorbances,
                mode='lines',
                name=f"{spectrum.experiment_id} (相似度: {score:.3f})",
                line=dict(color=color, width=2),
                opacity=0.8,
                hovertemplate=(
                    f'<b>{spectrum.experiment_id}</b><br>' +
                    f'相似度: {score:.3f}<br>' +
                    '波长: %{x:.1f} nm<br>' +
                    '吸光度: %{y:.4f}<br>' +
                    '<extra></extra>'
                )
            ))
        
        # 设置图表布局
        fig.update_layout(
            title=f"最相似的{top_n}个光谱 ({method.value.upper()})",
            xaxis_title="波长 (nm)",
            yaxis_title="吸光度",
            showlegend=True,
            hovermode='closest',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def _apply_filters(self, spectra: List[SpectralData], 
                      filter_settings: FilterSettings) -> List[SpectralData]:
        """
        应用筛选设置
        
        Args:
            spectra: 原始光谱数据
            filter_settings: 筛选设置
            
        Returns:
            筛选后的光谱数据
        """
        filtered_spectra = spectra
        
        # 波长范围筛选
        if filter_settings.wavelength_min is not None or filter_settings.wavelength_max is not None:
            filtered_spectra = []
            for spectrum in spectra:
                mask = np.ones(len(spectrum.wavelengths), dtype=bool)
                
                if filter_settings.wavelength_min is not None:
                    mask &= spectrum.wavelengths >= filter_settings.wavelength_min
                
                if filter_settings.wavelength_max is not None:
                    mask &= spectrum.wavelengths <= filter_settings.wavelength_max
                
                if np.any(mask):
                    filtered_spectrum = SpectralData(
                        wavelengths=spectrum.wavelengths[mask],
                        absorbances=spectrum.absorbances[mask],
                        experiment_id=spectrum.experiment_id,
                        metadata=spectrum.metadata
                    )
                    filtered_spectra.append(filtered_spectrum)
        
        # 实验ID筛选
        if filter_settings.experiment_ids:
            filtered_spectra = [s for s in filtered_spectra 
                              if s.experiment_id in filter_settings.experiment_ids]
        
        return filtered_spectra


def create_interactive_chart(figure: go.Figure) -> go.Figure:
    """
    为图表添加交互功能
    
    Args:
        figure: 原始图表
        
    Returns:
        增强交互功能的图表
    """
    # 添加选择工具
    figure.update_layout(
        dragmode='select',
        selectdirection='any'
    )
    
    # 添加缩放和平移按钮
    figure.update_layout(
        modebar_add=[
            'pan',
            'zoom',
            'reset+autorange',
            'select',
            'lasso2d'
        ]
    )
    
    return figure


def display_chart_options() -> PlotOptions:
    """显示图表选项设置"""
    st.subheader("图表设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("图表标题", value="UV-Vis光谱数据")
        x_label = st.text_input("X轴标签", value="波长 (nm)")
        y_label = st.text_input("Y轴标签", value="吸光度")
    
    with col2:
        show_legend = st.checkbox("显示图例", value=True)
        color_scheme = st.selectbox(
            "颜色方案",
            options=['plotly', 'set1', 'set2', 'set3', 'tab10', 'tab20'],
            index=0
        )
        line_width = st.slider("线条宽度", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
        opacity = st.slider("透明度", min_value=0.1, max_value=1.0, value=0.8, step=0.1)
    
    return PlotOptions(
        title=title,
        x_label=x_label,
        y_label=y_label,
        show_legend=show_legend,
        color_scheme=color_scheme,
        line_width=line_width,
        opacity=opacity
    )


def display_filter_options(spectra: List[SpectralData]) -> FilterSettings:
    """显示筛选选项设置"""
    if not spectra:
        return FilterSettings()
    
    st.subheader("数据筛选")
    
    # 获取波长范围
    all_wavelengths = np.concatenate([s.wavelengths for s in spectra])
    wavelength_min = float(all_wavelengths.min())
    wavelength_max = float(all_wavelengths.max())
    
    col1, col2 = st.columns(2)
    
    with col1:
        wavelength_min_filter = st.number_input(
            "最小波长 (nm)",
            min_value=wavelength_min,
            max_value=wavelength_max,
            value=wavelength_min,
            step=1.0
        )
        
        # 实验ID多选
        experiment_ids = [s.experiment_id for s in spectra]
        selected_experiments = st.multiselect(
            "选择实验",
            options=experiment_ids,
            default=experiment_ids
        )
    
    with col2:
        wavelength_max_filter = st.number_input(
            "最大波长 (nm)",
            min_value=wavelength_min,
            max_value=wavelength_max,
            value=wavelength_max,
            step=1.0
        )
        
        # 相似度阈值筛选
        similarity_threshold = st.number_input(
            "相似度阈值",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
    
    return FilterSettings(
        wavelength_min=wavelength_min_filter,
        wavelength_max=wavelength_max_filter,
        experiment_ids=selected_experiments if selected_experiments else None,
        similarity_threshold=similarity_threshold
    )
