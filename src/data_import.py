"""
数据导入模块
负责CSV文件读取、数据验证和预处理
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
import streamlit as st
from .utils import (
    SpectralData, ValidationResult, validate_wavelength_data, 
    validate_absorbance_data, interpolate_spectra
)


class DataImporter:
    """数据导入器"""
    
    def __init__(self):
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.supported_formats = ['.csv']
    
    def load_csv_file(self, file_path: str) -> List[SpectralData]:
        """
        加载CSV文件并解析为光谱数据
        
        Args:
            file_path: CSV文件路径
            
        Returns:
            光谱数据列表
        """
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 验证数据格式
            if df.shape[1] < 2:
                raise ValueError("CSV文件至少需要两列：波长列和至少一个吸光度列")
            
            # 提取波长数据（第一列）
            wavelengths = df.iloc[:, 0].values.astype(float)
            
            # 验证波长数据
            wavelength_validation = validate_wavelength_data(wavelengths)
            if not wavelength_validation.is_valid:
                raise ValueError(f"波长数据验证失败: {'; '.join(wavelength_validation.errors)}")
            
            # 提取光谱数据
            spectra = []
            for i in range(1, df.shape[1]):
                column_name = df.columns[i]
                absorbances = df.iloc[:, i].values.astype(float)
                
                # 验证吸光度数据
                absorbance_validation = validate_absorbance_data(absorbances)
                if not absorbance_validation.is_valid:
                    st.warning(f"列 {column_name} 吸光度数据验证失败: {'; '.join(absorbance_validation.errors)}")
                    continue
                
                # 创建光谱数据对象
                spectrum = SpectralData(
                    wavelengths=wavelengths,
                    absorbances=absorbances,
                    experiment_id=column_name,
                    metadata={
                        'column_index': i,
                        'warnings': absorbance_validation.warnings
                    }
                )
                spectra.append(spectrum)
            
            return spectra
            
        except Exception as e:
            raise ValueError(f"文件读取失败: {str(e)}")
    
    def validate_data(self, data: List[SpectralData]) -> ValidationResult:
        """
        验证光谱数据
        
        Args:
            data: 光谱数据列表
            
        Returns:
            验证结果
        """
        result = ValidationResult(True)
        
        if not data:
            result.add_error("没有有效的光谱数据")
            return result
        
        # 检查数据一致性
        reference_wavelengths = data[0].wavelengths
        for i, spectrum in enumerate(data[1:], 1):
            if not np.array_equal(spectrum.wavelengths, reference_wavelengths):
                result.add_warning(f"光谱 {spectrum.experiment_id} 的波长范围与其他光谱不一致")
        
        # 检查实验ID唯一性
        experiment_ids = [s.experiment_id for s in data]
        if len(experiment_ids) != len(set(experiment_ids)):
            result.add_warning("存在重复的实验ID")
        
        return result
    
    def preprocess_data(self, data: List[SpectralData], 
                       normalize: bool = True,
                       interpolate: bool = False,
                       target_wavelengths: Optional[np.ndarray] = None) -> List[SpectralData]:
        """
        预处理光谱数据
        
        Args:
            data: 原始光谱数据
            normalize: 是否标准化
            interpolate: 是否插值到统一波长范围
            target_wavelengths: 目标波长范围
            
        Returns:
            预处理后的光谱数据
        """
        processed_data = data.copy()
        
        # 标准化
        if normalize:
            processed_data = [spectrum.normalize() for spectrum in processed_data]
        
        # 插值到统一波长范围
        if interpolate and target_wavelengths is not None:
            processed_data = interpolate_spectra(processed_data, target_wavelengths)
        
        return processed_data
    
    def get_data_preview(self, data: List[SpectralData], 
                        max_rows: int = None) -> pd.DataFrame:
        """
        获取数据预览
        
        Args:
            data: 光谱数据列表
            max_rows: 最大显示行数，None表示显示全部数据
            
        Returns:
            预览数据框
        """
        if not data:
            return pd.DataFrame()
        
        # 创建预览数据框
        if max_rows is None:
            # 显示全部数据
            preview_data = {'Wavelength': data[0].wavelengths}
            for spectrum in data:
                preview_data[spectrum.experiment_id] = spectrum.absorbances
        else:
            # 显示指定行数
            preview_data = {'Wavelength': data[0].wavelengths[:max_rows]}
            for spectrum in data:
                preview_data[spectrum.experiment_id] = spectrum.absorbances[:max_rows]
        
        return pd.DataFrame(preview_data)
    
    def get_data_statistics(self, data: List[SpectralData]) -> dict:
        """
        获取数据统计信息
        
        Args:
            data: 光谱数据列表
            
        Returns:
            统计信息字典
        """
        if not data:
            return {}
        
        stats = {
            'total_spectra': len(data),
            'wavelength_range': {
                'min': float(data[0].wavelengths.min()),
                'max': float(data[0].wavelengths.max()),
                'step': float(np.mean(np.diff(data[0].wavelengths)))
            },
            'experiment_ids': [s.experiment_id for s in data],
            'data_shape': {
                'wavelengths': data[0].wavelengths.shape[0],
                'spectra': len(data)
            }
        }
        
        # 计算吸光度统计
        all_absorbances = np.concatenate([s.absorbances for s in data])
        stats['absorbance_stats'] = {
            'mean': float(np.mean(all_absorbances)),
            'std': float(np.std(all_absorbances)),
            'min': float(np.min(all_absorbances)),
            'max': float(np.max(all_absorbances))
        }
        
        return stats


def upload_file_widget() -> Optional[Tuple[str, bytes]]:
    """
    Streamlit文件上传组件
    
    Returns:
        文件名和文件内容的元组，如果未上传则返回None
    """
    uploaded_file = st.file_uploader(
        "选择CSV文件",
        type=['csv'],
        help="支持CSV格式的UV-Vis光谱数据文件"
    )
    
    if uploaded_file is not None:
        return uploaded_file.name, uploaded_file.getvalue()
    
    return None


def display_data_preview(data: List[SpectralData]):
    """显示数据预览"""
    if not data:
        st.info("请先上传数据文件")
        return
    
    st.subheader("数据预览")
    
    # 显示统计信息
    importer = DataImporter()
    stats = importer.get_data_statistics(data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("光谱数量", stats['total_spectra'])
    with col2:
        st.metric("波长范围", f"{stats['wavelength_range']['min']:.1f} - {stats['wavelength_range']['max']:.1f} nm")
    with col3:
        st.metric("数据点数", stats['data_shape']['wavelengths'])
    
    # 显示数据表格
    preview_df = importer.get_data_preview(data, max_rows=None)  # 显示全部数据
    st.dataframe(preview_df, use_container_width=True)
    
    # 删除实验列表显示，让界面更紧凑


def display_validation_results(validation: ValidationResult):
    """显示验证结果"""
    if not validation.is_valid:
        st.error("数据验证失败")
        for error in validation.errors:
            st.error(f"❌ {error}")
    
    if validation.warnings:
        st.warning("数据验证警告")
        for warning in validation.warnings:
            st.warning(f"⚠️ {warning}")
    
    if validation.is_valid and not validation.warnings:
        st.success("✅ 数据验证通过")
