#!/usr/bin/env python3
"""
简化的UI修改测试
"""

def test_app_structure():
    """测试应用程序结构"""
    print("🧪 测试应用程序结构...")
    
    try:
        # 检查app.py文件是否存在
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键修改
        checks = [
            ("标签页数量", content.count('st.tabs([') == 1, "应该只有一组标签页定义"),
            ("数据可视化标签页", '"📈 数据可视化"' in content, "应该包含数据可视化标签页"),
            ("相似度分析标签页", '"🔍 相似度分析"' in content, "应该包含相似度分析标签页"),
            ("数据导出标签页", '"📤 数据导出"' not in content, "不应该包含独立的数据导出标签页"),
            ("导出光谱数据功能", "导出光谱数据" in content, "应该包含导出光谱数据功能"),
            ("导出相似度结果功能", "导出相似度结果" in content, "应该包含导出相似度结果功能"),
            ("display_export_tab函数", "def display_export_tab" not in content, "应该删除display_export_tab函数")
        ]
        
        all_passed = True
        for check_name, result, description in checks:
            if result:
                print(f"✅ {check_name}: {description}")
            else:
                print(f"❌ {check_name}: {description}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_data_import_structure():
    """测试数据导入模块结构"""
    print("\n🧪 测试数据导入模块结构...")
    
    try:
        with open('src/data_import.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否删除了实验列表显示（在display_data_preview函数中）
        if "st.subheader(\"实验列表\")" not in content and "实验ID列表" not in content:
            print("✅ 实验列表显示已删除")
            return True
        else:
            print("❌ 实验列表显示仍然存在")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 UVKit UI修改验证")
    print("=" * 50)
    
    tests = [
        test_app_structure,
        test_data_import_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 UI修改验证成功！")
        print("\n📝 修改总结:")
        print("✅ 删除了'实验列表'显示")
        print("✅ 将'导出光谱数据'功能合并到'数据可视化'标签页")
        print("✅ 将'导出相似度结果'功能合并到'相似度分析'标签页")
        print("✅ 删除了独立的'数据导出'标签页")
        print("✅ 界面更加紧凑，用户体验更好")
        print("\n🚀 现在可以运行 'streamlit run app.py' 来启动应用")
    else:
        print("❌ 部分修改验证失败，请检查代码。")

if __name__ == "__main__":
    main()
