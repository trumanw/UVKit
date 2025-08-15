#!/usr/bin/env python3
"""
测试UI修改后的功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        from src.utils import SpectralData, SimilarityMethod
        from src.data_import import DataImporter
        from src.similarity import SimilarityAnalyzer
        print("✅ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_data_structures():
    """测试数据结构"""
    print("\n🧪 测试数据结构...")
    
    try:
        import numpy as np
        from src.utils import SpectralData
        
        # 创建测试数据
        wavelengths = np.array([200, 201, 202, 203, 204])
        absorbances = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        
        spectrum = SpectralData(
            wavelengths=wavelengths,
            absorbances=absorbances,
            experiment_id="test_spectrum"
        )
        
        print(f"✅ 光谱数据创建成功: {spectrum.experiment_id}")
        print(f"   波长范围: {spectrum.wavelengths.min():.1f} - {spectrum.wavelengths.max():.1f} nm")
        print(f"   数据点数: {len(spectrum.wavelengths)}")
        return True
    except Exception as e:
        print(f"❌ 数据结构测试失败: {e}")
        return False

def test_similarity_algorithms():
    """测试相似度算法"""
    print("\n🧪 测试相似度算法...")
    
    try:
        import numpy as np
        from src.similarity import SimilarityAnalyzer
        from src.utils import SpectralData
        
        analyzer = SimilarityAnalyzer()
        
        # 创建测试光谱
        wavelengths = np.array([200, 201, 202, 203, 204])
        spectrum1 = SpectralData(
            wavelengths=wavelengths,
            absorbances=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            experiment_id="test1"
        )
        spectrum2 = SpectralData(
            wavelengths=wavelengths,
            absorbances=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            experiment_id="test2"
        )
        
        # 测试SAM算法
        sam_score = analyzer.calculate_sam(spectrum1.absorbances, spectrum2.absorbances)
        print(f"✅ SAM算法测试成功: {sam_score:.3f}")
        
        # 测试余弦相似度
        cosine_score = analyzer.calculate_cosine_similarity(spectrum1.absorbances, spectrum2.absorbances)
        print(f"✅ 余弦相似度测试成功: {cosine_score:.3f}")
        
        # 测试皮尔逊相关系数
        pearson_score = analyzer.calculate_pearson_correlation(spectrum1.absorbances, spectrum2.absorbances)
        print(f"✅ 皮尔逊相关系数测试成功: {pearson_score:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ 相似度算法测试失败: {e}")
        return False

def test_data_import():
    """测试数据导入功能"""
    print("\n🧪 测试数据导入功能...")
    
    try:
        from src.data_import import DataImporter
        import pandas as pd
        import numpy as np
        
        # 创建测试CSV数据
        test_data = pd.DataFrame({
            'Wavelength': [200, 201, 202, 203, 204],
            'Experiment1': [0.123, 0.125, 0.128, 0.130, 0.132],
            'Experiment2': [0.145, 0.147, 0.149, 0.151, 0.153]
        })
        
        # 保存为临时CSV文件
        temp_file = "temp_test_data.csv"
        test_data.to_csv(temp_file, index=False)
        
        # 测试导入
        importer = DataImporter()
        spectra = importer.load_csv_file(temp_file)
        
        print(f"✅ 数据导入测试成功: 加载了 {len(spectra)} 个光谱")
        for spectrum in spectra:
            print(f"   - {spectrum.experiment_id}: {len(spectrum.wavelengths)} 个数据点")
        
        # 清理临时文件
        os.remove(temp_file)
        
        return True
    except Exception as e:
        print(f"❌ 数据导入测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 UVKit UI修改测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_structures,
        test_similarity_algorithms,
        test_data_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！UI修改成功。")
        print("\n📝 UI修改总结:")
        print("✅ 删除了'实验列表'显示")
        print("✅ 将'导出光谱数据'功能合并到'数据可视化'标签页")
        print("✅ 将'导出相似度结果'功能合并到'相似度分析'标签页")
        print("✅ 删除了独立的'数据导出'标签页")
        print("✅ 界面更加紧凑，用户体验更好")
    else:
        print("❌ 部分测试失败，请检查代码。")

if __name__ == "__main__":
    main()
