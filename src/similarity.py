"""
相似度分析模块
实现Spectral Angle Mapper、余弦相似度、皮尔逊相关系数三种算法
"""

import numpy as np
from typing import List, Optional, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
import streamlit as st
from .utils import (
    SpectralData, SimilarityResult, SimilarityMethod, 
    ValidationResult, interpolate_spectra
)


class SimilarityAnalyzer:
    """相似度分析器"""
    
    def __init__(self):
        self.supported_methods = [
            SimilarityMethod.SAM,
            SimilarityMethod.COSINE,
            SimilarityMethod.PEARSON
        ]
    
    def calculate_sam(self, spectrum1: np.ndarray, spectrum2: np.ndarray) -> float:
        """
        计算Spectral Angle Mapper (SAM) 相似度
        
        Args:
            spectrum1: 第一个光谱数据
            spectrum2: 第二个光谱数据
            
        Returns:
            SAM相似度值 (0-1之间，1表示完全相同)
        """
        # 避免除零错误
        if np.all(spectrum1 == 0) or np.all(spectrum2 == 0):
            return 0.0
        
        # 计算向量点积
        dot_product = np.dot(spectrum1, spectrum2)
        
        # 计算向量模长
        norm1 = np.linalg.norm(spectrum1)
        norm2 = np.linalg.norm(spectrum2)
        
        # 避免除零错误
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # 计算余弦值
        cosine_value = dot_product / (norm1 * norm2)
        
        # 限制余弦值范围，避免数值误差
        cosine_value = np.clip(cosine_value, -1.0, 1.0)
        
        # 计算角度（弧度）
        angle = np.arccos(cosine_value)
        
        # 转换为相似度值 (0-1)
        similarity = 1.0 - (angle / np.pi)
        
        return float(similarity)
    
    def calculate_cosine_similarity(self, spectrum1: np.ndarray, spectrum2: np.ndarray) -> float:
        """
        计算余弦相似度
        
        Args:
            spectrum1: 第一个光谱数据
            spectrum2: 第二个光谱数据
            
        Returns:
            余弦相似度值 (-1到1之间，1表示完全相同)
        """
        # 避免除零错误
        if np.all(spectrum1 == 0) or np.all(spectrum2 == 0):
            return 0.0
        
        # 计算向量点积
        dot_product = np.dot(spectrum1, spectrum2)
        
        # 计算向量模长
        norm1 = np.linalg.norm(spectrum1)
        norm2 = np.linalg.norm(spectrum2)
        
        # 避免除零错误
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # 计算余弦相似度
        similarity = dot_product / (norm1 * norm2)
        
        # 限制范围，避免数值误差
        similarity = np.clip(similarity, -1.0, 1.0)
        
        return float(similarity)
    
    def calculate_pearson_correlation(self, spectrum1: np.ndarray, spectrum2: np.ndarray) -> float:
        """
        计算皮尔逊相关系数
        
        Args:
            spectrum1: 第一个光谱数据
            spectrum2: 第二个光谱数据
            
        Returns:
            皮尔逊相关系数 (-1到1之间，1表示完全正相关)
        """
        try:
            # 使用scipy计算皮尔逊相关系数
            correlation, _ = pearsonr(spectrum1, spectrum2)
            
            # 处理NaN值
            if np.isnan(correlation):
                return 0.0
            
            return float(correlation)
            
        except Exception:
            # 如果计算失败，返回0
            return 0.0
    
    def calculate_similarity(self, spectra: List[SpectralData], 
                           reference: SpectralData, 
                           method: SimilarityMethod) -> np.ndarray:
        """
        计算所有光谱与参考光谱的相似度
        
        Args:
            spectra: 光谱数据列表
            reference: 参考光谱
            method: 相似度计算方法
            
        Returns:
            相似度分数数组
        """
        if not spectra:
            return np.array([])
        
        # 确保所有光谱具有相同的波长范围
        target_wavelengths = reference.wavelengths
        interpolated_spectra = interpolate_spectra(spectra, target_wavelengths)
        interpolated_reference = interpolate_spectra([reference], target_wavelengths)[0]
        
        scores = []
        
        for spectrum in interpolated_spectra:
            if method == SimilarityMethod.SAM:
                score = self.calculate_sam(spectrum.absorbances, interpolated_reference.absorbances)
            elif method == SimilarityMethod.COSINE:
                score = self.calculate_cosine_similarity(spectrum.absorbances, interpolated_reference.absorbances)
            elif method == SimilarityMethod.PEARSON:
                score = self.calculate_pearson_correlation(spectrum.absorbances, interpolated_reference.absorbances)
            else:
                raise ValueError(f"不支持的相似度方法: {method}")
            
            scores.append(score)
        
        return np.array(scores)
    
    def batch_calculate(self, spectra: List[SpectralData], 
                       reference: SpectralData) -> SimilarityResult:
        """
        批量计算所有三种相似度算法
        
        Args:
            spectra: 光谱数据列表
            reference: 参考光谱
            
        Returns:
            包含三种算法结果的相似度结果对象
        """
        if not spectra:
            raise ValueError("没有光谱数据可供分析")
        
        # 计算三种算法的相似度
        sam_scores = self.calculate_similarity(spectra, reference, SimilarityMethod.SAM)
        cosine_scores = self.calculate_similarity(spectra, reference, SimilarityMethod.COSINE)
        pearson_scores = self.calculate_similarity(spectra, reference, SimilarityMethod.PEARSON)
        
        # 创建结果对象
        result = SimilarityResult(
            sam_scores=sam_scores,
            cosine_scores=cosine_scores,
            pearson_scores=pearson_scores,
            experiment_ids=[s.experiment_id for s in spectra],
            reference_id=reference.experiment_id
        )
        
        return result
    
    def compare_algorithms(self, spectra: List[SpectralData], 
                          reference: SpectralData) -> dict:
        """
        比较三种算法的性能
        
        Args:
            spectra: 光谱数据列表
            reference: 参考光谱
            
        Returns:
            算法比较结果字典
        """
        # 计算所有算法的结果
        result = self.batch_calculate(spectra, reference)
        
        # 计算统计信息
        comparison = {
            'sam': {
                'mean': float(np.mean(result.sam_scores)),
                'std': float(np.std(result.sam_scores)),
                'min': float(np.min(result.sam_scores)),
                'max': float(np.max(result.sam_scores)),
                'median': float(np.median(result.sam_scores))
            },
            'cosine': {
                'mean': float(np.mean(result.cosine_scores)),
                'std': float(np.std(result.cosine_scores)),
                'min': float(np.min(result.cosine_scores)),
                'max': float(np.max(result.cosine_scores)),
                'median': float(np.median(result.cosine_scores))
            },
            'pearson': {
                'mean': float(np.mean(result.pearson_scores)),
                'std': float(np.std(result.pearson_scores)),
                'min': float(np.min(result.pearson_scores)),
                'max': float(np.max(result.pearson_scores)),
                'median': float(np.median(result.pearson_scores))
            }
        }
        
        # 计算算法间的相关性
        comparison['correlations'] = {
            'sam_cosine': float(np.corrcoef(result.sam_scores, result.cosine_scores)[0, 1]),
            'sam_pearson': float(np.corrcoef(result.sam_scores, result.pearson_scores)[0, 1]),
            'cosine_pearson': float(np.corrcoef(result.cosine_scores, result.pearson_scores)[0, 1])
        }
        
        return comparison
    
    def get_top_similar_spectra(self, result: SimilarityResult, 
                               method: SimilarityMethod, 
                               top_n: int = 10) -> List[Tuple[str, float]]:
        """
        获取最相似的top_n个光谱
        
        Args:
            result: 相似度计算结果
            method: 相似度方法
            top_n: 返回前n个结果
            
        Returns:
            最相似光谱的列表，每个元素为(实验ID, 相似度分数)
        """
        return result.get_top_similar(method, top_n)
    
    def validate_reference_spectrum(self, reference: SpectralData, 
                                  spectra: List[SpectralData]) -> ValidationResult:
        """
        验证参考光谱的有效性
        
        Args:
            reference: 参考光谱
            spectra: 待比较的光谱列表
            
        Returns:
            验证结果
        """
        result = ValidationResult(True)
        
        # 检查参考光谱是否为空
        if reference is None:
            result.add_error("参考光谱不能为空")
            return result
        
        # 检查波长范围是否与待比较光谱一致
        if spectra:
            ref_wavelengths = reference.wavelengths
            sample_wavelengths = spectra[0].wavelengths
            
            ref_min, ref_max = ref_wavelengths.min(), ref_wavelengths.max()
            sample_min, sample_max = sample_wavelengths.min(), sample_wavelengths.max()
            
            if ref_min > sample_max or ref_max < sample_min:
                result.add_warning("参考光谱的波长范围与待比较光谱不重叠")
        
        return result


def display_similarity_results(result: SimilarityResult):
    """显示相似度分析结果"""
    if not result:
        st.info("请先进行相似度分析")
        return
    
    st.subheader("相似度分析结果")
    
    # 创建结果数据框
    results_df = pd.DataFrame({
        '实验ID': result.experiment_ids,
        'SAM相似度': result.sam_scores,
        '余弦相似度': result.cosine_scores,
        '皮尔逊相关系数': result.pearson_scores
    })
    
    # 显示结果表格
    st.dataframe(results_df, use_container_width=True)
    
    # 显示统计信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("SAM平均相似度", f"{np.mean(result.sam_scores):.3f}")
    with col2:
        st.metric("余弦平均相似度", f"{np.mean(result.cosine_scores):.3f}")
    with col3:
        st.metric("皮尔逊平均相关系数", f"{np.mean(result.pearson_scores):.3f}")


def display_algorithm_comparison(comparison: dict):
    """显示算法比较结果"""
    if not comparison:
        return
    
    st.subheader("算法性能比较")
    
    # 创建比较表格
    comparison_data = []
    for method, stats in comparison.items():
        if method != 'correlations':
            comparison_data.append({
                '算法': method.upper(),
                '平均值': f"{stats['mean']:.3f}",
                '标准差': f"{stats['std']:.3f}",
                '最小值': f"{stats['min']:.3f}",
                '最大值': f"{stats['max']:.3f}",
                '中位数': f"{stats['median']:.3f}"
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    # 显示算法间相关性
    if 'correlations' in comparison:
        st.subheader("算法间相关性")
        correlations = comparison['correlations']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("SAM-余弦", f"{correlations['sam_cosine']:.3f}")
        with col2:
            st.metric("SAM-皮尔逊", f"{correlations['sam_pearson']:.3f}")
        with col3:
            st.metric("余弦-皮尔逊", f"{correlations['cosine_pearson']:.3f}")


def select_reference_spectrum(spectra: List[SpectralData]) -> Optional[SpectralData]:
    """选择参考光谱"""
    if not spectra:
        return None
    
    experiment_ids = [s.experiment_id for s in spectra]
    
    selected_id = st.selectbox(
        "选择参考光谱",
        experiment_ids,
        help="选择作为相似度计算基准的参考光谱"
    )
    
    if selected_id:
        return next(s for s in spectra if s.experiment_id == selected_id)
    
    return None
