"""
UVKit - UV-Vis光谱数据分析与可视化平台
主应用程序入口
"""

import streamlit as st
import pandas as pd
import numpy as np
import tempfile
import os
from typing import List, Optional

# 导入自定义模块
from src.data_import import DataImporter, upload_file_widget, display_data_preview
from src.similarity import SimilarityAnalyzer, select_reference_spectrum
from src.utils import SpectralData, SimilarityMethod

# 页面配置
st.set_page_config(
    page_title="UVKit - UV-Vis光谱数据分析",
    page_icon="📊",
    layout="wide"
)

def main():
    """主应用程序函数"""
    
    # 页面标题
    st.title("UVKit - UV-Vis光谱数据分析与可视化平台")
    
    # 初始化会话状态
    if 'spectral_data' not in st.session_state:
        st.session_state.spectral_data = None
    if 'similarity_results' not in st.session_state:
        st.session_state.similarity_results = None
    
    # 侧边栏
    with st.sidebar:
        st.header("📁 数据上传")
        
        # 文件上传
        file_info = upload_file_widget()
        
        if file_info:
            filename, file_content = file_info
            
            # 保存上传的文件到临时目录
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            try:
                # 加载数据
                importer = DataImporter()
                spectral_data = importer.load_csv_file(tmp_file_path)
                st.session_state.spectral_data = spectral_data
                st.success(f"✅ 成功加载 {len(spectral_data)} 个光谱数据")
                
            except Exception as e:
                st.error(f"❌ 文件加载失败: {str(e)}")
            finally:
                # 清理临时文件
                os.unlink(tmp_file_path)
    
    # 主内容区域
    if st.session_state.spectral_data:
        # 创建标签页
        tab1, tab2 = st.tabs(["📈 数据可视化", "🔍 相似度分析"])
        
        with tab1:
            display_visualization_tab()
        
        with tab2:
            display_similarity_tab()
    
    else:
        # 显示欢迎信息
        st.markdown("""
        ## 🎯 欢迎使用UVKit
        
        UVKit是一个专业的UV-Vis光谱数据分析与可视化平台。
        
        ### 🚀 主要功能
        - 批量数据导入
        - 多算法相似度分析
        - 交互式可视化
        - 数据筛选和导出
        
        ### 📄 数据格式要求
        CSV文件格式：
        - 第一列：波长数据（单位：nm）
        - 第二列开始：各实验的吸光度数据
        
        ### 💡 开始使用
        请在左侧边栏上传您的CSV数据文件开始分析。
        """)

def display_visualization_tab():
    """显示数据可视化标签页"""
    st.header("📈 数据可视化")
    
    if st.session_state.spectral_data:
        # 显示数据预览
        display_data_preview(st.session_state.spectral_data)
        
        # 简单的光谱图
        st.subheader("光谱曲线")
        data = st.session_state.spectral_data
        
        # 创建简单的图表
        chart_data = pd.DataFrame({
            'Wavelength': data[0].wavelengths,
            **{s.experiment_id: s.absorbances for s in data}
        })
        
        st.line_chart(chart_data.set_index('Wavelength'))
        
        # 导出光谱数据功能
        st.subheader("📤 导出光谱数据")
        
        # 创建数据框
        df = pd.DataFrame({
            'Wavelength': data[0].wavelengths,
            **{s.experiment_id: s.absorbances for s in data}
        })
        
        # CSV导出
        csv = df.to_csv(index=False)
        st.download_button(
            label="下载CSV文件",
            data=csv,
            file_name="spectral_data.csv",
            mime="text/csv"
        )

def display_similarity_tab():
    """显示相似度分析标签页"""
    st.header("🔍 相似度分析")
    
    if st.session_state.spectral_data:
        # 选择参考光谱
        reference_spectrum = select_reference_spectrum(st.session_state.spectral_data)
        
        if reference_spectrum:
            st.success(f"✅ 已选择参考光谱: {reference_spectrum.experiment_id}")
            
            if st.button("🚀 开始相似度分析", type="primary"):
                with st.spinner("正在计算相似度..."):
                    # 创建分析器
                    analyzer = SimilarityAnalyzer()
                    
                    # 执行批量计算
                    similarity_results = analyzer.batch_calculate(
                        st.session_state.spectral_data, 
                        reference_spectrum
                    )
                    
                    st.session_state.similarity_results = similarity_results
                    st.success("✅ 相似度分析完成")
                    
                    # 显示结果
                    st.subheader("分析结果")
                    results_df = pd.DataFrame({
                        '实验ID': similarity_results.experiment_ids,
                        'SAM相似度': similarity_results.sam_scores,
                        '余弦相似度': similarity_results.cosine_scores,
                        '皮尔逊相关系数': similarity_results.pearson_scores
                    })
                    st.dataframe(results_df, use_container_width=True)
                    
                    # 导出相似度结果功能
                    st.subheader("📤 导出相似度结果")
                    csv_results = results_df.to_csv(index=False)
                    st.download_button(
                        label="下载相似度结果CSV",
                        data=csv_results,
                        file_name="similarity_results.csv",
                        mime="text/csv"
                    )
        else:
            st.info("ℹ️ 请选择一个参考光谱进行分析")

# 删除display_export_tab函数，因为功能已经合并到其他标签页

if __name__ == "__main__":
    main()
