#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自定义配置文件解析器
"""

from config import CustomConfigParser, load_config


def test_parser():
    """测试配置文件解析器"""
    parser = CustomConfigParser()

    print("=== 测试1: 解析示例配置文件 ===")
    try:
        config = parser.parse_file('example_config.ccf')
        print("配置文件解析成功！")

        # 显示解析结果
        for section, items in config.items():
            print(f"\n[{section}]")
            for key, value in items.items():
                print(f"  {key} = {value} ({type(value).__name__})")

        print("\n" + "="*50)

        # 测试访问特定配置
        print("=== 测试2: 访问配置值 ===")
        app_name = parser.get('application', 'name')
        server_port = parser.get('server', 'port')
        debug_mode = parser.get('application', 'debug')

        print(f"应用名称: {app_name}")
        print(f"服务器端口: {server_port}")
        print(f"调试模式: {debug_mode}")

        # 测试默认值
        print(f"默认值测试: {parser.get('nonexistent', 'key', 'default_value')}")

        print("\n" + "="*50)

        # 测试快捷函数
        print("=== 测试3: 快捷函数 load_config ===")
        config2 = load_config('example_config.ccf')
        print(f"快捷函数加载结果: {'成功' if config == config2 else '失败'}")

        print("\n" + "="*50)

        # 测试写入功能
        print("=== 测试4: 测试写入配置功能 ===")
        test_config = {
            'test_section': {
                'string_value': 'Hello World',
                'int_value': 42,
                'float_value': 3.14,
                'bool_value': True,
                'list_value': ['item1', 'item2', 'item3'],
                'dict_value': {'key1': 'value1', 'key2': 123}
            }
        }

        parser.write_config('test_output.ccf', test_config)
        print("配置写入 test_output.ccf 成功！")

        # 验证写入的内容
        loaded_config = parser.parse_file('test_output.ccf')
        print("重新加载验证成功！")

        for section, items in loaded_config.items():
            print(f"\n[{section}]")
            for key, value in items.items():
                print(f"  {key} = {value} ({type(value).__name__})")

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_advanced_features():
    """测试高级特性"""
    print("\n" + "="*50)
    print("=== 测试5: 高级特性测试 ===")

    test_content = """## 高级特性测试配置

[advanced]
## 多行字符串
multiline_text = "这是第一行\n这是第二行\n这是第三行"

## 特殊字符
special_chars = "包含Tab字符：\t和特殊符号!@#$%"

## 表达式
startup_cmd = expr:systemctl start perflaunch.service

## 路径
log_path = path:/var/log/perflaunch/app.log

## 嵌套数据结构
complex_data = {name: "test", values: [1, 2, 3], config: {debug: yes, timeout: 30}}

## 混合列表
mixed_list = ["string", 123, yes, {nested: value}]
"""

    parser = CustomConfigParser()
    config = parser.parse_string(test_content)

    print("高级配置解析结果:")
    for section, items in config.items():
        print(f"\n[{section}]")
        for key, value in items.items():
            print(f"  {key} = {repr(value)} ({type(value).__name__})")


if __name__ == "__main__":
    test_parser()
    test_advanced_features()

    print("\n" + "="*50)
    print("所有测试完成！配置文件格式已验证成功。")
    print("你可以使用 load_config('文件名.ccf') 来加载配置文件")
    print("或者直接使用 CustomConfigParser() 类进行更灵活的操作")