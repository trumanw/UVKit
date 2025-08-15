"""
UVKit - UV-Vis光谱数据分析与可视化平台

主要模块：
- data_import: 数据导入模块
- similarity: 相似度分析模块
- visualization: 可视化模块
- filter: 数据筛选模块
- export: 数据导出模块
- utils: 工具函数
"""

__version__ = "1.0.0"
__author__ = "UVKit Team"
__email__ = "support@uvkit.com"

from .data_import import DataImporter
from .similarity import SimilarityAnalyzer
from .visualization import SpectrumVisualizer
from .filter import DataFilter
from .export import DataExporter
from .utils import SpectralData, SimilarityResult, AnalysisResult

__all__ = [
    'DataImporter',
    'SimilarityAnalyzer', 
    'SpectrumVisualizer',
    'DataFilter',
    'DataExporter',
    'SpectralData',
    'SimilarityResult',
    'AnalysisResult'
]
