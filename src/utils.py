"""
工具函数和数据结构定义
"""

from typing import List, Dict, Optional, Union, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass
from enum import Enum


class SimilarityMethod(Enum):
    """相似度计算方法枚举"""
    SAM = "sam"
    COSINE = "cosine"
    PEARSON = "pearson"


@dataclass
class SpectralData:
    """光谱数据结构"""
    wavelengths: np.ndarray
    absorbances: np.ndarray
    experiment_id: str
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def shape(self) -> Tuple[int, int]:
        """返回光谱数据形状"""
        return self.wavelengths.shape[0], self.absorbances.shape[0]
    
    def normalize(self) -> 'SpectralData':
        """数据标准化"""
        if np.max(self.absorbances) > 0:
            normalized_absorbances = self.absorbances / np.max(self.absorbances)
        else:
            normalized_absorbances = self.absorbances
        return SpectralData(
            wavelengths=self.wavelengths,
            absorbances=normalized_absorbances,
            experiment_id=self.experiment_id,
            metadata=self.metadata
        )


@dataclass
class SimilarityResult:
    """相似度计算结果"""
    sam_scores: np.ndarray
    cosine_scores: np.ndarray
    pearson_scores: np.ndarray
    experiment_ids: List[str]
    reference_id: str
    
    def get_score(self, method: SimilarityMethod) -> np.ndarray:
        """获取指定方法的相似度分数"""
        if method == SimilarityMethod.SAM:
            return self.sam_scores
        elif method == SimilarityMethod.COSINE:
            return self.cosine_scores
        elif method == SimilarityMethod.PEARSON:
            return self.pearson_scores
        else:
            raise ValueError(f"不支持的相似度方法: {method}")
    
    def get_top_similar(self, method: SimilarityMethod, top_n: int = 10) -> List[Tuple[str, float]]:
        """获取最相似的top_n个实验"""
        scores = self.get_score(method)
        indices = np.argsort(scores)[::-1][:top_n]
        return [(self.experiment_ids[i], scores[i]) for i in indices]


@dataclass
class FilterSettings:
    """筛选设置"""
    wavelength_min: Optional[float] = None
    wavelength_max: Optional[float] = None
    experiment_ids: Optional[List[str]] = None
    similarity_threshold: Optional[float] = None
    similarity_method: Optional[SimilarityMethod] = None


@dataclass
class PlotOptions:
    """绘图选项"""
    title: str = "UV-Vis光谱数据"
    x_label: str = "波长 (nm)"
    y_label: str = "吸光度"
    show_legend: bool = True
    color_scheme: str = "plotly"
    line_width: float = 2.0
    opacity: float = 0.8


@dataclass
class AnalysisResult:
    """分析结果"""
    spectral_data: List[SpectralData]
    similarity_results: Optional[SimilarityResult] = None
    filter_settings: Optional[FilterSettings] = None
    plot_options: Optional[PlotOptions] = None


class ValidationResult:
    """数据验证结果"""
    
    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
    
    def add_error(self, error: str):
        """添加错误信息"""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str):
        """添加警告信息"""
        self.warnings.append(warning)


class ExportResult:
    """导出结果"""
    
    def __init__(self, success: bool, file_path: str = None, error: str = None):
        self.success = success
        self.file_path = file_path
        self.error = error


def validate_wavelength_data(wavelengths: np.ndarray) -> ValidationResult:
    """验证波长数据"""
    result = ValidationResult(True)
    
    # 检查数据类型
    if not np.issubdtype(wavelengths.dtype, np.number):
        result.add_error("波长数据必须为数值类型")
    
    # 检查数值范围
    if np.any(wavelengths < 0):
        result.add_error("波长值不能为负数")
    
    if np.any(wavelengths > 1000):
        result.add_warning("波长值超过1000nm，请确认数据正确性")
    
    # 检查单调性
    if not np.all(np.diff(wavelengths) > 0):
        result.add_error("波长数据必须单调递增")
    
    return result


def validate_absorbance_data(absorbances: np.ndarray) -> ValidationResult:
    """验证吸光度数据"""
    result = ValidationResult(True)
    
    # 检查数据类型
    if not np.issubdtype(absorbances.dtype, np.number):
        result.add_error("吸光度数据必须为数值类型")
    
    # 检查数值范围
    if np.any(absorbances < 0):
        result.add_warning("存在负吸光度值，请确认数据正确性")
    
    if np.any(absorbances > 10):
        result.add_warning("存在大于10的吸光度值，请确认数据正确性")
    
    # 检查异常值
    mean_abs = np.mean(absorbances)
    std_abs = np.std(absorbances)
    outliers = np.abs(absorbances - mean_abs) > 3 * std_abs
    if np.any(outliers):
        result.add_warning(f"检测到{np.sum(outliers)}个可能的异常值")
    
    return result


def interpolate_spectra(spectra: List[SpectralData], 
                       target_wavelengths: np.ndarray) -> List[SpectralData]:
    """将光谱数据插值到统一的波长范围"""
    interpolated_spectra = []
    
    for spectrum in spectra:
        # 使用线性插值
        interpolated_absorbances = np.interp(
            target_wavelengths, 
            spectrum.wavelengths, 
            spectrum.absorbances
        )
        
        interpolated_spectrum = SpectralData(
            wavelengths=target_wavelengths,
            absorbances=interpolated_absorbances,
            experiment_id=spectrum.experiment_id,
            metadata=spectrum.metadata
        )
        interpolated_spectra.append(interpolated_spectrum)
    
    return interpolated_spectra


def calculate_statistics(spectra: List[SpectralData]) -> Dict:
    """计算光谱数据统计信息"""
    if not spectra:
        return {}
    
    all_absorbances = np.concatenate([s.absorbances for s in spectra])
    
    stats = {
        'total_spectra': len(spectra),
        'wavelength_range': {
            'min': min(s.wavelengths.min() for s in spectra),
            'max': max(s.wavelengths.max() for s in spectra)
        },
        'absorbance_stats': {
            'mean': float(np.mean(all_absorbances)),
            'std': float(np.std(all_absorbances)),
            'min': float(np.min(all_absorbances)),
            'max': float(np.max(all_absorbances))
        }
    }
    
    return stats
