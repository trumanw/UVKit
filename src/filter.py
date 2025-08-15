"""
数据筛选模块
负责波长范围、实验编号、相似度阈值等筛选功能
"""

import numpy as np
from typing import List, Optional
from .utils import SpectralData, FilterSettings, SimilarityResult, SimilarityMethod


class DataFilter:
    """数据筛选器"""
    
    def __init__(self):
        pass
    
    def filter_by_wavelength(self, data: List[SpectralData], 
                           min_wavelength: float, 
                           max_wavelength: float) -> List[SpectralData]:
        """
        按波长范围筛选数据
        
        Args:
            data: 光谱数据列表
            min_wavelength: 最小波长
            max_wavelength: 最大波长
            
        Returns:
            筛选后的光谱数据列表
        """
        filtered_data = []
        
        for spectrum in data:
            # 创建波长范围掩码
            mask = (spectrum.wavelengths >= min_wavelength) & (spectrum.wavelengths <= max_wavelength)
            
            if np.any(mask):
                # 创建筛选后的光谱数据
                filtered_spectrum = SpectralData(
                    wavelengths=spectrum.wavelengths[mask],
                    absorbances=spectrum.absorbances[mask],
                    experiment_id=spectrum.experiment_id,
                    metadata=spectrum.metadata
                )
                filtered_data.append(filtered_spectrum)
        
        return filtered_data
    
    def filter_by_experiment(self, data: List[SpectralData], 
                           experiment_ids: List[str]) -> List[SpectralData]:
        """
        按实验ID筛选数据
        
        Args:
            data: 光谱数据列表
            experiment_ids: 要保留的实验ID列表
            
        Returns:
            筛选后的光谱数据列表
        """
        return [spectrum for spectrum in data if spectrum.experiment_id in experiment_ids]
    
    def filter_by_similarity(self, data: List[SpectralData], 
                           similarity_results: SimilarityResult, 
                           threshold: float,
                           method: SimilarityMethod) -> List[SpectralData]:
        """
        按相似度阈值筛选数据
        
        Args:
            data: 光谱数据列表
            similarity_results: 相似度计算结果
            threshold: 相似度阈值
            method: 相似度计算方法
            
        Returns:
            筛选后的光谱数据列表
        """
        if not similarity_results:
            return data
        
        # 获取相似度分数
        scores = similarity_results.get_score(method)
        
        # 找到满足阈值条件的实验ID
        valid_indices = np.where(scores >= threshold)[0]
        valid_ids = [similarity_results.experiment_ids[i] for i in valid_indices]
        
        # 筛选数据
        return self.filter_by_experiment(data, valid_ids)
    
    def apply_multiple_filters(self, data: List[SpectralData], 
                              filter_settings: FilterSettings,
                              similarity_results: Optional[SimilarityResult] = None) -> List[SpectralData]:
        """
        应用多个筛选条件
        
        Args:
            data: 光谱数据列表
            filter_settings: 筛选设置
            similarity_results: 相似度计算结果（可选）
            
        Returns:
            筛选后的光谱数据列表
        """
        filtered_data = data.copy()
        
        # 波长范围筛选
        if filter_settings.wavelength_min is not None or filter_settings.wavelength_max is not None:
            min_wl = filter_settings.wavelength_min if filter_settings.wavelength_min is not None else float('-inf')
            max_wl = filter_settings.wavelength_max if filter_settings.wavelength_max is not None else float('inf')
            filtered_data = self.filter_by_wavelength(filtered_data, min_wl, max_wl)
        
        # 实验ID筛选
        if filter_settings.experiment_ids:
            filtered_data = self.filter_by_experiment(filtered_data, filter_settings.experiment_ids)
        
        # 相似度阈值筛选
        if (filter_settings.similarity_threshold is not None and 
            filter_settings.similarity_method is not None and 
            similarity_results is not None):
            filtered_data = self.filter_by_similarity(
                filtered_data, 
                similarity_results, 
                filter_settings.similarity_threshold,
                filter_settings.similarity_method
            )
        
        return filtered_data
    
    def get_filter_statistics(self, original_data: List[SpectralData], 
                            filtered_data: List[SpectralData]) -> dict:
        """
        获取筛选统计信息
        
        Args:
            original_data: 原始数据
            filtered_data: 筛选后数据
            
        Returns:
            统计信息字典
        """
        original_count = len(original_data)
        filtered_count = len(filtered_data)
        
        stats = {
            'original_count': original_count,
            'filtered_count': filtered_count,
            'removed_count': original_count - filtered_count,
            'retention_rate': filtered_count / original_count if original_count > 0 else 0
        }
        
        return stats
