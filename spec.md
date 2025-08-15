# UVKit - UV-Vis光谱数据分析与可视化程序
## 软件功能模块设计规格文档

---

## 1. 系统架构设计

### 1.1 整体架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户界面层     │    │   业务逻辑层     │    │   数据处理层     │
│   (Streamlit)   │◄──►│   (Python)      │◄──►│   (Pandas/NumPy)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   可视化组件     │    │   算法引擎       │    │   文件处理       │
│   (Plotly)      │    │   (Scikit-learn)│    │   (CSV/Excel)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 模块划分
- **UI模块**：用户界面和交互逻辑
- **数据处理模块**：CSV文件读取、数据验证、预处理
- **算法模块**：光谱相似度计算算法
- **可视化模块**：图表生成和展示
- **导出模块**：结果导出功能

---

## 2. 功能模块详细设计

### 2.1 数据导入模块 (Data Import Module)

#### 2.1.1 模块职责
- CSV文件上传和解析
- 数据格式验证
- 数据预处理和标准化
- 错误处理和用户反馈

#### 2.1.2 核心功能
**CSV文件解析器**
- 输入：CSV文件流
- 输出：结构化光谱数据
- 处理逻辑：
  1. 读取CSV文件内容
  2. 验证第一列为波长数据
  3. 提取光谱数据列
  4. 数据类型转换和验证

**数据验证器**
- 波长数据验证：连续性检查、数值范围验证
- 吸光度数据验证：数值有效性、异常值检测
- 数据完整性检查：缺失值处理

**数据预处理器**
- 波长对齐：统一波长范围和步长
- 数据标准化：归一化处理
- 异常值处理：平滑或插值

#### 2.1.3 接口设计
```python
class DataImporter:
    def load_csv_file(file_path: str) -> SpectralData
    def validate_data(data: SpectralData) -> ValidationResult
    def preprocess_data(data: SpectralData) -> SpectralData
    def get_data_preview(data: SpectralData) -> DataFrame
```

### 2.2 光谱相似度分析模块 (Spectral Similarity Module)

#### 2.2.1 模块职责
- 实现三种相似度算法
- 批量相似度计算
- 算法性能优化
- 结果统计和分析

#### 2.2.2 核心算法实现

**Spectral Angle Mapper (SAM)**
```python
def calculate_sam(spectrum1: np.array, spectrum2: np.array) -> float:
    # 计算两个光谱向量之间的夹角余弦值
    # 返回0-1之间的相似度值
```

**余弦相似度 (Cosine Similarity)**
```python
def calculate_cosine_similarity(spectrum1: np.array, spectrum2: np.array) -> float:
    # 计算两个光谱向量的余弦相似度
    # 返回-1到1之间的相似度值
```

**皮尔逊相关系数 (Pearson Correlation)**
```python
def calculate_pearson_correlation(spectrum1: np.array, spectrum2: np.array) -> float:
    # 计算两个光谱数据的线性相关性
    # 返回-1到1之间的相关系数
```

#### 2.2.3 批量计算引擎
- 并行计算支持
- 内存优化
- 进度跟踪
- 结果缓存

#### 2.2.4 接口设计
```python
class SimilarityAnalyzer:
    def calculate_similarity(spectra: List[SpectralData], 
                           reference: SpectralData, 
                           method: str) -> SimilarityResult
    def batch_calculate(spectra: List[SpectralData], 
                       reference: SpectralData) -> BatchResult
    def compare_algorithms(spectra: List[SpectralData], 
                          reference: SpectralData) -> ComparisonResult
```

### 2.3 数据可视化模块 (Visualization Module)

#### 2.3.1 模块职责
- 光谱曲线绘制
- 相似度结果可视化
- 交互式图表功能
- 图表导出

#### 2.3.2 核心组件

**光谱曲线绘制器**
- 多光谱同时显示
- 颜色方案管理
- 图例和标签
- 坐标轴配置

**相似度结果可视化器**
- 相似度分布直方图
- 算法对比图表
- 排序列表展示
- 阈值筛选可视化

**交互式功能**
- 缩放和平移
- 数据点悬停信息
- 曲线选择和高亮
- 动态筛选

#### 2.3.3 接口设计
```python
class SpectrumVisualizer:
    def plot_spectra(spectra: List[SpectralData], 
                    options: PlotOptions) -> PlotlyFigure
    def plot_similarity_results(results: SimilarityResult, 
                               options: PlotOptions) -> PlotlyFigure
    def create_interactive_chart(figure: PlotlyFigure) -> InteractiveChart
```

### 2.4 数据筛选模块 (Filter Module)

#### 2.4.1 模块职责
- 波长范围筛选
- 实验编号筛选
- 相似度阈值筛选
- 多条件组合筛选

#### 2.4.2 筛选器类型

**波长筛选器**
- 波长范围选择
- 波长步长调整
- 特定波长点选择

**实验筛选器**
- 实验编号列表
- 实验名称搜索
- 批量选择/取消

**相似度筛选器**
- 阈值设置
- 多算法阈值
- 动态筛选

#### 2.4.3 接口设计
```python
class DataFilter:
    def filter_by_wavelength(data: SpectralData, 
                           min_wavelength: float, 
                           max_wavelength: float) -> SpectralData
    def filter_by_experiment(data: SpectralData, 
                           experiment_ids: List[str]) -> SpectralData
    def filter_by_similarity(data: SpectralData, 
                           similarity_results: SimilarityResult, 
                           threshold: float) -> SpectralData
    def apply_multiple_filters(data: SpectralData, 
                              filters: List[Filter]) -> SpectralData
```

### 2.5 数据导出模块 (Export Module)

#### 2.5.1 模块职责
- 分析结果导出
- 图表导出
- 多种格式支持
- 导出进度管理

#### 2.5.2 导出功能

**数据导出**
- Excel格式 (.xlsx)
- CSV格式 (.csv)
- JSON格式 (.json)

**图表导出**
- PNG图片
- SVG矢量图
- PDF文档

**报告导出**
- 综合分析报告
- 自定义模板
- 批量导出

#### 2.5.3 接口设计
```python
class DataExporter:
    def export_data(data: SpectralData, 
                   format: str, 
                   file_path: str) -> ExportResult
    def export_chart(chart: PlotlyFigure, 
                    format: str, 
                    file_path: str) -> ExportResult
    def generate_report(data: SpectralData, 
                       results: AnalysisResult, 
                       template: str) -> Report
```

---

## 3. 用户界面设计

### 3.1 页面布局结构

#### 3.1.1 主页面布局
```
┌─────────────────────────────────────────────────────────────┐
│                        UVKit                                │
├─────────────────┬───────────────────────────────────────────┤
│   侧边栏        │              主内容区域                    │
│   - 数据上传    │   - 数据可视化图表                        │
│   - 参数设置    │   - 分析结果展示                          │
│   - 筛选条件    │   - 交互式操作区域                        │
│   - 导出选项    │                                           │
└─────────────────┴───────────────────────────────────────────┘
```

#### 3.1.2 页面组件设计

**侧边栏组件**
- 文件上传区域
- 参数配置面板
- 筛选条件设置
- 导出选项配置

**主内容区域**
- 光谱曲线显示区域
- 相似度分析结果区域
- 数据统计信息区域
- 操作日志区域

### 3.2 交互流程设计

#### 3.2.1 主要用户流程
1. **数据上传流程**
   - 选择CSV文件
   - 数据预览和验证
   - 确认导入

2. **分析流程**
   - 选择参考光谱
   - 选择相似度算法
   - 执行批量计算
   - 查看结果

3. **可视化流程**
   - 选择显示选项
   - 应用筛选条件
   - 交互式操作
   - 导出结果

#### 3.2.2 错误处理流程
- 文件格式错误提示
- 数据验证失败处理
- 计算错误恢复
- 用户操作指导

---

## 4. 数据结构设计

### 4.1 核心数据结构

#### 4.1.1 光谱数据类
```python
class SpectralData:
    wavelengths: np.array      # 波长数据
    absorbances: np.array      # 吸光度数据
    experiment_id: str         # 实验标识
    metadata: dict            # 元数据信息
```

#### 4.1.2 相似度结果类
```python
class SimilarityResult:
    sam_scores: np.array      # SAM算法结果
    cosine_scores: np.array   # 余弦相似度结果
    pearson_scores: np.array  # 皮尔逊相关系数结果
    experiment_ids: List[str] # 实验标识列表
    reference_id: str         # 参考光谱标识
```

#### 4.1.3 分析结果类
```python
class AnalysisResult:
    spectral_data: SpectralData
    similarity_results: SimilarityResult
    filter_settings: FilterSettings
    visualization_options: VisualizationOptions
```

### 4.2 配置数据结构

#### 4.2.1 应用配置
```python
class AppConfig:
    max_file_size: int        # 最大文件大小
    supported_formats: List[str]  # 支持的文件格式
    default_plot_options: PlotOptions  # 默认绘图选项
    export_formats: List[str] # 支持的导出格式
```

---

## 5. 性能优化设计

### 5.1 数据处理优化
- **内存管理**：大数据集的分块处理
- **并行计算**：多核CPU利用
- **缓存机制**：计算结果缓存
- **数据压缩**：临时数据压缩存储

### 5.2 算法优化
- **向量化计算**：NumPy向量化操作
- **算法选择**：根据数据规模选择最优算法
- **预计算**：常用计算结果预存储
- **增量计算**：支持增量更新

### 5.3 用户界面优化
- **异步处理**：长时间操作异步执行
- **进度反馈**：实时进度显示
- **响应式设计**：界面自适应调整
- **懒加载**：按需加载数据

---

## 6. 错误处理设计

### 6.1 错误分类
- **文件错误**：格式错误、大小超限、损坏文件
- **数据错误**：格式不匹配、缺失值、异常值
- **计算错误**：算法失败、内存不足、超时
- **用户错误**：操作失误、参数错误

### 6.2 错误处理策略
- **预防性检查**：输入验证、参数检查
- **优雅降级**：部分功能失效时的处理
- **用户指导**：错误原因说明和解决建议
- **日志记录**：错误信息记录和分析

---

## 7. 测试策略

### 7.1 单元测试
- 各模块功能测试
- 算法准确性验证
- 边界条件测试
- 异常情况处理

### 7.2 集成测试
- 模块间接口测试
- 数据流测试
- 端到端功能测试
- 性能测试

### 7.3 用户测试
- 界面易用性测试
- 功能完整性测试
- 用户体验测试
- 兼容性测试

---

## 8. 部署和配置

### 8.1 环境要求
- Python 3.8+
- 依赖包管理
- 系统资源要求
- 浏览器兼容性

### 8.2 部署方案
- 本地部署
- 容器化部署
- 云端部署
- 配置管理

### 8.3 监控和维护
- 性能监控
- 错误日志
- 用户反馈
- 版本更新

---

## 9. 安全考虑

### 9.1 数据安全
- 本地数据处理
- 临时文件清理
- 数据加密存储
- 访问权限控制

### 9.2 系统安全
- 输入验证
- 文件安全检查
- 异常处理
- 安全日志

---

## 10. 扩展性设计

### 10.1 算法扩展
- 插件化算法架构
- 新算法接口定义
- 算法参数配置
- 性能评估框架

### 10.2 功能扩展
- 模块化设计
- 插件系统
- API接口
- 第三方集成

### 10.3 平台扩展
- 移动端适配
- 云端服务
- 分布式处理
- 多用户支持
```
