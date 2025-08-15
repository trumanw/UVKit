"""
数据导出模块
负责分析结果和图表的多格式导出
"""

import pandas as pd
import numpy as np
import os
from typing import List, Optional, Dict
import streamlit as st
from .utils import (
    SpectralData, SimilarityResult, SimilarityMethod, 
    ExportResult, AnalysisResult
)


class DataExporter:
    """数据导出器"""
    
    def __init__(self):
        self.supported_formats = {
            'data': ['csv', 'xlsx', 'json'],
            'chart': ['png', 'svg', 'html'],
            'report': ['pdf', 'html']
        }
    
    def export_data(self, data: List[SpectralData], 
                   format: str, 
                   file_path: str) -> ExportResult:
        """
        导出光谱数据
        
        Args:
            data: 光谱数据列表
            format: 导出格式 ('csv', 'xlsx', 'json')
            file_path: 文件路径
            
        Returns:
            导出结果
        """
        try:
            if not data:
                return ExportResult(False, error="没有数据可导出")
            
            # 创建数据框
            df = self._create_dataframe(data)
            
            if format.lower() == 'csv':
                df.to_csv(file_path, index=False)
            elif format.lower() == 'xlsx':
                df.to_excel(file_path, index=False, engine='openpyxl')
            elif format.lower() == 'json':
                df.to_json(file_path, orient='records', indent=2)
            else:
                return ExportResult(False, error=f"不支持的格式: {format}")
            
            return ExportResult(True, file_path=file_path)
            
        except Exception as e:
            return ExportResult(False, error=str(e))
    
    def export_similarity_results(self, result: SimilarityResult, 
                                format: str, 
                                file_path: str) -> ExportResult:
        """
        导出相似度分析结果
        
        Args:
            result: 相似度计算结果
            format: 导出格式
            file_path: 文件路径
            
        Returns:
            导出结果
        """
        try:
            if not result:
                return ExportResult(False, error="没有相似度结果可导出")
            
            # 创建结果数据框
            results_df = pd.DataFrame({
                '实验ID': result.experiment_ids,
                'SAM相似度': result.sam_scores,
                '余弦相似度': result.cosine_scores,
                '皮尔逊相关系数': result.pearson_scores
            })
            
            if format.lower() == 'csv':
                results_df.to_csv(file_path, index=False)
            elif format.lower() == 'xlsx':
                results_df.to_excel(file_path, index=False, engine='openpyxl')
            elif format.lower() == 'json':
                results_df.to_json(file_path, orient='records', indent=2)
            else:
                return ExportResult(False, error=f"不支持的格式: {format}")
            
            return ExportResult(True, file_path=file_path)
            
        except Exception as e:
            return ExportResult(False, error=str(e))
    
    def export_chart(self, chart, 
                    format: str, 
                    file_path: str) -> ExportResult:
        """
        导出图表
        
        Args:
            chart: Plotly图表对象
            format: 导出格式 ('png', 'svg', 'html')
            file_path: 文件路径
            
        Returns:
            导出结果
        """
        try:
            if format.lower() == 'png':
                chart.write_image(file_path, width=1200, height=800)
            elif format.lower() == 'svg':
                chart.write_image(file_path, format='svg')
            elif format.lower() == 'html':
                chart.write_html(file_path)
            else:
                return ExportResult(False, error=f"不支持的图表格式: {format}")
            
            return ExportResult(True, file_path=file_path)
            
        except Exception as e:
            return ExportResult(False, error=str(e))
    
    def generate_report(self, data: List[SpectralData], 
                       results: Optional[SimilarityResult], 
                       template: str = "basic") -> str:
        """
        生成分析报告
        
        Args:
            data: 光谱数据
            results: 相似度分析结果
            template: 报告模板
            
        Returns:
            报告内容
        """
        report_lines = []
        
        # 报告标题
        report_lines.append("# UV-Vis光谱数据分析报告")
        report_lines.append("")
        
        # 数据概览
        report_lines.append("## 数据概览")
        report_lines.append(f"- 光谱数量: {len(data)}")
        if data:
            wavelengths = data[0].wavelengths
            report_lines.append(f"- 波长范围: {wavelengths.min():.1f} - {wavelengths.max():.1f} nm")
            report_lines.append(f"- 数据点数: {len(wavelengths)}")
        report_lines.append("")
        
        # 实验列表
        report_lines.append("## 实验列表")
        for i, spectrum in enumerate(data, 1):
            report_lines.append(f"{i}. {spectrum.experiment_id}")
        report_lines.append("")
        
        # 相似度分析结果
        if results:
            report_lines.append("## 相似度分析结果")
            report_lines.append("")
            
            # 统计信息
            report_lines.append("### 统计信息")
            report_lines.append(f"- SAM平均相似度: {np.mean(results.sam_scores):.3f}")
            report_lines.append(f"- 余弦平均相似度: {np.mean(results.cosine_scores):.3f}")
            report_lines.append(f"- 皮尔逊平均相关系数: {np.mean(results.pearson_scores):.3f}")
            report_lines.append("")
            
            # 最相似的光谱
            report_lines.append("### 最相似的光谱 (SAM)")
            top_similar = results.get_top_similar(SimilarityMethod.SAM, 5)
            for i, (exp_id, score) in enumerate(top_similar, 1):
                report_lines.append(f"{i}. {exp_id}: {score:.3f}")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _create_dataframe(self, data: List[SpectralData]) -> pd.DataFrame:
        """
        从光谱数据创建数据框
        
        Args:
            data: 光谱数据列表
            
        Returns:
            Pandas数据框
        """
        if not data:
            return pd.DataFrame()
        
        # 创建数据字典
        df_dict = {'Wavelength': data[0].wavelengths}
        
        # 添加每个光谱的吸光度数据
        for spectrum in data:
            df_dict[spectrum.experiment_id] = spectrum.absorbances
        
        return pd.DataFrame(df_dict)


def create_download_button(data: bytes, 
                          file_name: str, 
                          button_text: str = "下载文件"):
    """
    创建Streamlit下载按钮
    
    Args:
        data: 文件数据
        file_name: 文件名
        button_text: 按钮文本
    """
    st.download_button(
        label=button_text,
        data=data,
        file_name=file_name,
        mime="application/octet-stream"
    )


def export_data_widget(data: List[SpectralData], 
                      similarity_results: Optional[SimilarityResult] = None):
    """
    数据导出组件
    
    Args:
        data: 光谱数据
        similarity_results: 相似度分析结果
    """
    st.subheader("数据导出")
    
    exporter = DataExporter()
    
    # 导出选项
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**导出光谱数据**")
        data_format = st.selectbox(
            "数据格式",
            options=['csv', 'xlsx', 'json'],
            key="data_format"
        )
        
        if st.button("导出光谱数据"):
            if data:
                # 创建临时文件
                temp_file = f"spectral_data.{data_format}"
                result = exporter.export_data(data, data_format, temp_file)
                
                if result.success:
                    with open(temp_file, 'rb') as f:
                        file_data = f.read()
                    
                    create_download_button(
                        file_data,
                        f"spectral_data.{data_format}",
                        f"下载光谱数据 ({data_format.upper()})"
                    )
                    
                    # 清理临时文件
                    os.remove(temp_file)
                else:
                    st.error(f"导出失败: {result.error}")
            else:
                st.warning("没有数据可导出")
    
    with col2:
        st.write("**导出相似度结果**")
        if similarity_results:
            sim_format = st.selectbox(
                "结果格式",
                options=['csv', 'xlsx', 'json'],
                key="sim_format"
            )
            
            if st.button("导出相似度结果"):
                temp_file = f"similarity_results.{sim_format}"
                result = exporter.export_similarity_results(
                    similarity_results, sim_format, temp_file
                )
                
                if result.success:
                    with open(temp_file, 'rb') as f:
                        file_data = f.read()
                    
                    create_download_button(
                        file_data,
                        f"similarity_results.{sim_format}",
                        f"下载相似度结果 ({sim_format.upper()})"
                    )
                    
                    # 清理临时文件
                    os.remove(temp_file)
                else:
                    st.error(f"导出失败: {result.error}")
        else:
            st.info("请先进行相似度分析")


def export_chart_widget(chart):
    """
    图表导出组件
    
    Args:
        chart: Plotly图表对象
    """
    st.subheader("图表导出")
    
    exporter = DataExporter()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("导出为PNG"):
            if chart:
                temp_file = "chart.png"
                result = exporter.export_chart(chart, 'png', temp_file)
                
                if result.success:
                    with open(temp_file, 'rb') as f:
                        file_data = f.read()
                    
                    create_download_button(
                        file_data,
                        "chart.png",
                        "下载PNG图表"
                    )
                    
                    os.remove(temp_file)
                else:
                    st.error(f"导出失败: {result.error}")
            else:
                st.warning("没有图表可导出")
    
    with col2:
        if st.button("导出为SVG"):
            if chart:
                temp_file = "chart.svg"
                result = exporter.export_chart(chart, 'svg', temp_file)
                
                if result.success:
                    with open(temp_file, 'rb') as f:
                        file_data = f.read()
                    
                    create_download_button(
                        file_data,
                        "chart.svg",
                        "下载SVG图表"
                    )
                    
                    os.remove(temp_file)
                else:
                    st.error(f"导出失败: {result.error}")
            else:
                st.warning("没有图表可导出")
    
    with col3:
        if st.button("导出为HTML"):
            if chart:
                temp_file = "chart.html"
                result = exporter.export_chart(chart, 'html', temp_file)
                
                if result.success:
                    with open(temp_file, 'rb') as f:
                        file_data = f.read()
                    
                    create_download_button(
                        file_data,
                        "chart.html",
                        "下载HTML图表"
                    )
                    
                    os.remove(temp_file)
                else:
                    st.error(f"导出失败: {result.error}")
            else:
                st.warning("没有图表可导出")
