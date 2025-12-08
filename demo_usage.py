#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义配置文件格式演示 - 简化版
展示主要功能而不包含复杂的测试
"""

from custom_config import CustomConfigParser, load_config

def main():
    print("🎯 自定义配置文件格式 (.ccf) 演示")
    print("="*50)

    # 1. 加载并展示示例配置
    print("1️⃣ 加载配置文件...")
    config = load_config('example_config.ccf')

    # 显示几个关键配置
    app_name = config['application']['name']
    version = config['application']['version']
    server_port = config['server']['port']
    db_type = config['database']['type']

    print(f"📋 应用信息: {app_name} v{version}")
    print(f"🌐 服务器端口: {server_port}")
    print(f"🗄️  数据库类型: {db_type}")

    print("\n" + "="*50)

    # 2. 展示不同类型的配置值
    print("2️⃣ 配置数据类型演示:")

    parser = CustomConfigParser()
    sample_config = """
## 数据类型示例
[demo]
## 字符串
app_name = "MyApplication"

## 整数
max_users = 1000

## 浮点数
rate_limit = 50.5

## 布尔值
debug_enabled = yes
production_mode = no

## 列表
features = ["auth", "api", "websocket"]
ports = [80, 443, 8080]

## 字典
database = {host: "localhost", port: 5432, name: "mydb"}

## 特殊值
log_path = path:/var/log/myapp.log
startup_script = expr:start_application()
"""

    result = parser.parse_string(sample_config)

    for section, items in result.items():
        print(f"\n[{section}]")
        for key, value in items.items():
            print(f"  {key} = {value} ({type(value).__name__})")

    print("\n" + "="*50)

    # 3. 展示配置访问API
    print("3️⃣ 配置访问API演示:")
    print(f"使用便捷函数: app_name = {parser.get('demo', 'app_name')}")
    print(f"获取默认值: nonexistent = {parser.get('demo', 'nonexistent_key', 'default_value')}")
    print(f"获取整个段: database_config = {parser.get_section('demo')}")

    print("\n" + "="*50)
    print("✅ 演示完成！")
    print("\n💡 使用说明:")
    print("• 使用 load_config('文件.ccf') 快速加载配置")
    print("• 使用 CustomConfigParser() 进行高级操作")
    print("• 支持的文件扩展名: .ccf (Custom Config Format)")
    print("❌ 与主流格式完全不兼容 (JSON/YAML/INI/TOML)")

if __name__ == "__main__":
    main()