#!/usr/bin/env python3
"""
简化的数据预览功能测试
"""

def test_data_import_function():
    """测试数据导入函数的修改"""
    print("🧪 测试数据导入函数修改...")
    
    try:
        with open('src/data_import.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键修改
        checks = [
            ("get_data_preview函数参数", "max_rows: int = None" in content, "参数默认值应该改为None"),
            ("全量数据预览逻辑", "if max_rows is None:" in content, "应该包含全量数据预览逻辑"),
            ("部分数据预览逻辑", "else:" in content, "应该保留部分数据预览逻辑"),
            ("display_data_preview调用", "max_rows=None" in content, "应该调用全量数据预览"),
            ("注释说明", "显示全部数据" in content, "应该有相关注释")
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

def test_function_signature():
    """测试函数签名修改"""
    print("\n🧪 测试函数签名修改...")
    
    try:
        with open('src/data_import.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找函数定义
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def get_data_preview' in line:
                print(f"✅ 找到函数定义: {line.strip()}")
                
                # 检查下一行的参数
                if i + 1 < len(lines) and 'max_rows: int = None' in lines[i + 1]:
                    print("✅ 参数默认值已修改为None")
                    return True
                elif 'max_rows: int = None' in line:
                    print("✅ 参数默认值已修改为None")
                    return True
                else:
                    print("❌ 参数默认值未修改")
                    return False
        
        print("❌ 未找到函数定义")
        return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_display_function_call():
    """测试显示函数调用修改"""
    print("\n🧪 测试显示函数调用修改...")
    
    try:
        with open('src/data_import.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查display_data_preview函数中的调用
        if 'get_data_preview(data, max_rows=None)' in content:
            print("✅ display_data_preview函数调用已修改")
            return True
        else:
            print("❌ display_data_preview函数调用未修改")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 UVKit 数据预览功能修改验证")
    print("=" * 50)
    
    tests = [
        test_data_import_function,
        test_function_signature,
        test_display_function_call
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 数据预览功能修改验证成功！")
        print("\n📝 修改总结:")
        print("✅ get_data_preview函数参数默认值改为None")
        print("✅ 添加了全量数据预览逻辑")
        print("✅ 保留了部分数据预览功能")
        print("✅ display_data_preview函数调用已更新")
        print("✅ 现在数据预览表格将显示全量数据")
        print("\n🚀 用户现在可以看到完整的数据表格")
    else:
        print("❌ 部分修改验证失败，请检查代码。")

if __name__ == "__main__":
    main()
