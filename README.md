# UVKit - UV-Vis光谱数据分析与可视化平台

## 项目简介

UVKit是一个基于Web的UV-Vis光谱数据批量处理、分析和可视化工具，专为化学、材料科学等领域的科研人员设计。

## 主要功能

- **批量数据导入**：支持CSV格式的UV-Vis光谱数据批量导入
- **多算法相似度分析**：支持Spectral Angle Mapper、余弦相似度、皮尔逊相关系数三种算法
- **交互式可视化**：基于Plotly的交互式光谱曲线显示
- **智能数据筛选**：支持波长范围、实验编号、相似度阈值等多种筛选方式
- **多格式导出**：支持Excel、CSV、PNG、SVG等多种导出格式

## 技术栈

- **前端框架**：Streamlit
- **可视化库**：Plotly
- **数据处理**：Pandas, NumPy
- **算法实现**：Scikit-learn
- **文件处理**：openpyxl, xlsxwriter

## 安装和运行

### 环境要求
- Python 3.8+
- 推荐使用虚拟环境

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd UVKit
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
streamlit run app.py
```

5. 打开浏览器访问 http://localhost:8501

## 使用说明

### 数据格式要求

CSV文件格式：
- 第一列：波长数据（单位：nm）
- 第二列开始：各实验的吸光度数据
- 支持标准CSV格式，逗号分隔

示例：
```
Wavelength,Experiment1,Experiment2,Experiment3
200,0.123,0.145,0.167
201,0.125,0.147,0.169
...
```

### 主要操作流程

1. **数据上传**：在侧边栏上传CSV格式的光谱数据文件
2. **数据预览**：查看上传数据的格式和内容
3. **参考光谱选择**：上传或选择参考光谱数据
4. **相似度分析**：选择算法并执行批量相似度计算
5. **结果可视化**：查看光谱曲线和相似度分析结果
6. **数据筛选**：根据需要筛选显示的数据
7. **结果导出**：导出分析结果和图表

## 项目结构

```
UVKit/
├── app.py                 # 主应用程序入口
├── requirements.txt       # 项目依赖
├── README.md             # 项目说明
├── src/                  # 源代码目录
│   ├── __init__.py
│   ├── data_import.py    # 数据导入模块
│   ├── similarity.py     # 相似度分析模块
│   ├── visualization.py  # 可视化模块
│   ├── filter.py         # 数据筛选模块
│   ├── export.py         # 数据导出模块
│   └── utils.py          # 工具函数
├── data/                 # 示例数据目录
│   └── sample_data.csv   # 示例数据文件
├── tests/                # 测试目录
│   ├── __init__.py
│   ├── test_data_import.py
│   ├── test_similarity.py
│   └── test_visualization.py
└── docs/                 # 文档目录
    ├── user_guide.md     # 用户指南
    └── api_docs.md       # API文档
```

## 开发指南

### 代码规范
- 遵循PEP 8代码规范
- 使用类型注解
- 编写详细的文档字符串
- 添加单元测试

### 测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_similarity.py
```

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。
