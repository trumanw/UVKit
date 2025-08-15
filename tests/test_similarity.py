"""
相似度算法测试
"""

import unittest
import numpy as np
from src.similarity import SimilarityAnalyzer
from src.utils import SpectralData, SimilarityMethod


class TestSimilarityAnalyzer(unittest.TestCase):
    """相似度分析器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.analyzer = SimilarityAnalyzer()
        
        # 创建测试数据
        self.wavelengths = np.array([200, 201, 202, 203, 204])
        self.spectrum1 = SpectralData(
            wavelengths=self.wavelengths,
            absorbances=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            experiment_id="test1"
        )
        self.spectrum2 = SpectralData(
            wavelengths=self.wavelengths,
            absorbances=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            experiment_id="test2"
        )
        self.spectrum3 = SpectralData(
            wavelengths=self.wavelengths,
            absorbances=np.array([0.5, 0.4, 0.3, 0.2, 0.1]),
            experiment_id="test3"
        )
    
    def test_sam_calculation(self):
        """测试SAM算法计算"""
        # 相同光谱应该有最高相似度
        sam_score = self.analyzer.calculate_sam(
            self.spectrum1.absorbances, 
            self.spectrum2.absorbances
        )
        self.assertAlmostEqual(sam_score, 1.0, places=5)
        
        # 不同光谱应该有较低相似度
        sam_score = self.analyzer.calculate_sam(
            self.spectrum1.absorbances, 
            self.spectrum3.absorbances
        )
        self.assertLess(sam_score, 1.0)
        self.assertGreaterEqual(sam_score, 0.0)
    
    def test_cosine_similarity(self):
        """测试余弦相似度计算"""
        # 相同光谱应该有最高相似度
        cosine_score = self.analyzer.calculate_cosine_similarity(
            self.spectrum1.absorbances, 
            self.spectrum2.absorbances
        )
        self.assertAlmostEqual(cosine_score, 1.0, places=5)
        
        # 不同光谱应该有较低相似度
        cosine_score = self.analyzer.calculate_cosine_similarity(
            self.spectrum1.absorbances, 
            self.spectrum3.absorbances
        )
        self.assertLess(cosine_score, 1.0)
        self.assertGreaterEqual(cosine_score, -1.0)
    
    def test_pearson_correlation(self):
        """测试皮尔逊相关系数计算"""
        # 相同光谱应该有最高相关系数
        pearson_score = self.analyzer.calculate_pearson_correlation(
            self.spectrum1.absorbances, 
            self.spectrum2.absorbances
        )
        self.assertAlmostEqual(pearson_score, 1.0, places=5)
        
        # 不同光谱应该有较低相关系数
        pearson_score = self.analyzer.calculate_pearson_correlation(
            self.spectrum1.absorbances, 
            self.spectrum3.absorbances
        )
        self.assertLess(pearson_score, 1.0)
        self.assertGreaterEqual(pearson_score, -1.0)
    
    def test_batch_calculation(self):
        """测试批量计算"""
        spectra = [self.spectrum1, self.spectrum2, self.spectrum3]
        reference = self.spectrum1
        
        result = self.analyzer.batch_calculate(spectra, reference)
        
        # 检查结果格式
        self.assertEqual(len(result.sam_scores), 3)
        self.assertEqual(len(result.cosine_scores), 3)
        self.assertEqual(len(result.pearson_scores), 3)
        self.assertEqual(len(result.experiment_ids), 3)
        self.assertEqual(result.reference_id, "test1")
        
        # 检查第一个光谱（与参考相同）应该有最高相似度
        self.assertAlmostEqual(result.sam_scores[0], 1.0, places=5)
        self.assertAlmostEqual(result.cosine_scores[0], 1.0, places=5)
        self.assertAlmostEqual(result.pearson_scores[0], 1.0, places=5)


if __name__ == '__main__':
    unittest.main()
