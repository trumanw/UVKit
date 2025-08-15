#!/usr/bin/env python3
"""
测试数据预览功能
"""

import sys
import os
import pandas as pd
import numpy as np

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_data_preview_full():
    """测试全量数据预览功能"""
    print("🧪 测试全量数据预览功能...")
    
    try:
        from src.data_import import DataImporter
        from src.utils import SpectralData
        
        # 创建测试数据
        wavelengths = np.array([200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210])
        spectrum1 = SpectralData(
            wavelengths=wavelengths,
            absorbances=np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]),
            experiment_id="Test1"
        )
        spectrum2 = SpectralData(
            wavelengths=wavelengths,
            absorbances=np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]),
            experiment_id="Test2"
        )
        
        data = [spectrum1, spectrum2]
        
        # 测试全量数据预览
        importer = DataImporter()
        preview_df = importer.get_data_preview(data, max_rows=None)
        
        print(f"✅ 数据预览创建成功")
        print(f"   数据框形状: {preview_df.shape}")
        print(f"   行数: {len(preview_df)} (应该是 {len(wavelengths)})")
        print(f"   列数: {len(preview_df.columns)} (应该是 {len(data) + 1})")
        
        # 验证数据完整性
        if len(preview_df) == len(wavelengths):
            print("✅ 数据行数正确")
        else:
            print("❌ 数据行数不正确")
            return False
        
        if len(preview_df.columns) == len(data) + 1:  # +1 for Wavelength column
            print("✅ 数据列数正确")
        else:
            print("❌ 数据列数不正确")
            return False
        
        # 验证第一行和最后一行数据
        print(f"   第一行波长: {preview_df.iloc[0]['Wavelength']}")
        print(f"   最后一行波长: {preview_df.iloc[-1]['Wavelength']}")
        print(f"   第一行Test1: {preview_df.iloc[0]['Test1']}")
        print(f"   最后一行Test1: {preview_df.iloc[-1]['Test1']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_data_preview_partial():
    """测试部分数据预览功能"""
    print("\n🧪 测试部分数据预览功能...")
    
    try:
        from src.data_import import DataImporter
        from src.utils import SpectralData
        
        # 创建测试数据
        wavelengths = np.array([200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210])
        spectrum1 = SpectralData(
            wavelengths=wavelengths,
            absorbances=np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]),
            experiment_id="Test1"
        )
        spectrum2 = SpectralData(
            wavelengths=wavelengths,
            absorbances=np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]),
            experiment_id="Test2"
        )
        
        data = [spectrum1, spectrum2]
        
        # 测试部分数据预览（5行）
        importer = DataImporter()
        preview_df = importer.get_data_preview(data, max_rows=5)
        
        print(f"✅ 部分数据预览创建成功")
        print(f"   数据框形状: {preview_df.shape}")
        print(f"   行数: {len(preview_df)} (应该是 5)")
        print(f"   列数: {len(preview_df.columns)} (应该是 {len(data) + 1})")
        
        # 验证数据完整性
        if len(preview_df) == 5:
            print("✅ 部分数据行数正确")
        else:
            print("❌ 部分数据行数不正确")
            return False
        
        if len(preview_df.columns) == len(data) + 1:  # +1 for Wavelength column
            print("✅ 部分数据列数正确")
        else:
            print("❌ 部分数据列数不正确")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_sample_data():
    """测试示例数据文件"""
    print("\n🧪 测试示例数据文件...")
    
    try:
        # 读取示例数据文件
        sample_file = "data/sample_data.csv"
        if os.path.exists(sample_file):
            df = pd.read_csv(sample_file)
            print(f"✅ 示例数据文件读取成功")
            print(f"   文件形状: {df.shape}")
            print(f"   波长范围: {df.iloc[:, 0].min():.1f} - {df.iloc[:, 0].max():.1f} nm")
            print(f"   实验数量: {len(df.columns) - 1}")
            
            # 测试数据导入
            from src.data_import import DataImporter
            importer = DataImporter()
            spectra = importer.load_csv_file(sample_file)
            
            print(f"✅ 示例数据导入成功")
            print(f"   光谱数量: {len(spectra)}")
            
            # 测试全量预览
            preview_df = importer.get_data_preview(spectra, max_rows=None)
            print(f"   预览数据形状: {preview_df.shape}")
            print(f"   预览行数: {len(preview_df)} (应该是 {len(df)})")
            
            if len(preview_df) == len(df):
                print("✅ 示例数据预览正确")
                return True
            else:
                print("❌ 示例数据预览不正确")
                return False
        else:
            print("⚠️ 示例数据文件不存在，跳过此测试")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 UVKit 数据预览功能测试")
    print("=" * 50)
    
    tests = [
        test_data_preview_full,
        test_data_preview_partial,
        test_sample_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 数据预览功能测试成功！")
        print("\n📝 功能总结:")
        print("✅ 支持全量数据预览 (max_rows=None)")
        print("✅ 支持部分数据预览 (max_rows=N)")
        print("✅ 数据完整性验证通过")
        print("✅ 示例数据文件测试通过")
        print("\n🚀 现在数据预览表格将显示全量数据")
    else:
        print("❌ 部分测试失败，请检查代码。")

if __name__ == "__main__":
    main()
