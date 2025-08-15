#!/usr/bin/env python3
"""
UVKit 启动脚本
"""

import subprocess
import sys
import os

def main():
    """主函数"""
    print("🚀 启动 UVKit - UV-Vis光谱数据分析与可视化平台")
    print("=" * 60)
    
    # 检查依赖
    print("📦 检查依赖...")
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        import sklearn
        print("✅ 所有依赖已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return
    
    # 启动应用
    print("🌐 启动Web应用...")
    print("应用将在浏览器中打开: http://localhost:8501")
    print("按 Ctrl+C 停止应用")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
