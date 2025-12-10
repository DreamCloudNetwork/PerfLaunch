#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义配置文件解析器
采用独特的配置格式，与主流格式不兼容
"""

import re
from typing import Dict, Any, Union


class CustomConfigParser:
    """自定义配置文件解析器"""

    def __init__(self):
        self.config = {}

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """解析配置文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse_string(content)

    def parse_string(self, content: str) -> Dict[str, Any]:
        """解析配置字符串"""
        self.config = {}
        lines = content.strip().split('\n')

        current_section = None
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # 跳过空行和注释
            if not line or line.startswith('##'):
                continue

            # 解析段定义: [SECTION_NAME]
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                self.config[current_section] = {}
                continue

            # 解析键值对
            if '=' in line:
                key, value = self._parse_key_value(line)
                if current_section is None:
                    raise ValueError(f"第{line_num}行: 必须在段内定义键值对")

                self.config[current_section][key] = value
            else:
                # 忽略无法解析的行，而不是抛出错误
                continue

        return self.config

    def _parse_key_value(self, line: str) -> tuple:
        """解析键值对"""
        parts = line.split('=', 1)
        key = parts[0].strip()
        value = parts[1].strip()

        # 验证键名格式
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
            raise ValueError(f"无效的键名: {key}")

        # 根据值的格式进行解析
        return key, self._parse_value(value)

    def _parse_value(self, value: str) -> Union[str, int, float, bool, list, dict]:
        """解析不同类型的值"""
        # 字符串值 (有引号)
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')

        # 整数值
        if re.match(r'^\d+$', value):
            return int(value)

        # 小数值
        if re.match(r'^\d+\.\d+$', value):
            return float(value)

        # 布尔值
        if value.lower() in ['yes', 'true', 'on']:
            return True
        if value.lower() in ['no', 'false', 'off']:
            return False

        # 列表值 [item1, item2, item3]
        if value.startswith('[') and value.endswith(']'):
            items = value[1:-1].split(',')
            return [self._parse_value(item.strip()) for item in items if item.strip()]

        # 字典值 {key1: value1, key2: value2}
        if value.startswith('{') and value.endswith('}'):
            items = value[1:-1].split(',')
            result = {}
            for item in items:
                if ':' in item:
                    k, v = item.split(':', 1)
                    result[k.strip()] = self._parse_value(v.strip())
            return result

        # 路径值 (包含特殊前缀)
        if value.startswith('path:'):
            return value[5:]

        # 表达式值 (包含特殊前缀)
        if value.startswith('expr:'):
            return value[5:]  # 原样返回，使用时再解析

        # 默认作为字符串
        return value

    def get(self, section: str, key: str, default=None):
        """获取配置值"""
        return self.config.get(section, {}).get(key, default)

    def get_section(self, section: str, default=None):
        """获取整个段"""
        return self.config.get(section, default or {})

    def write_config(self, file_path: str, config_dict: Dict[str, Any]):
        """写入配置文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            for section, items in config_dict.items():
                f.write(f"[{section}]\n")
                for key, value in items.items():
                    formatted_value = self._format_value(value)
                    f.write(f"{key} = {formatted_value}\n")
                f.write("\n")

    def _format_value(self, value: Any) -> str:
        """格式化值为配置格式"""
        if isinstance(value, str):
            # 检查是否需要引号
            if ' ' in value or '\n' in value or '\t' in value or '"' in value:
                escaped = value.replace('\n', '\\n').replace('\t', '\\t').replace('"', '\\"')
                return f'"{escaped}"'
            return value
        elif isinstance(value, bool):
            return 'yes' if value else 'no'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            items = [self._format_value(item) for item in value]
            return f"[{', '.join(items)}]"
        elif isinstance(value, dict):
            items = [f"{k}: {self._format_value(v)}" for k, v in value.items()]
            return f"{{{', '.join(items)}}}"
        else:
            return str(value)


def load_config(file_path: str) -> Dict[str, Any]:
    """快捷函数：加载配置文件"""
    parser = CustomConfigParser()
    return parser.parse_file(file_path)


if __name__ == "__main__":
    # 测试解析器
    parser = CustomConfigParser()

    # 示例配置字符串
    sample_config = """
## 这是注释行，以双井号开始

[database]
host = "localhost"
port = 5432
username = "admin"
password = "secret123"
enabled = yes

cache_size = 1024
timeout = 30.5
backup_paths = ["/home/backup", "/var/backup"]
settings = {max_connections: 100, timeout: 30}

[server]
ip = "0.0.0.0"
port = 8080
workers = 4
debug = no

document_root = path:/var/www/html
startup_script = expr:init_server()
"""

    result = parser.parse_string(sample_config)
    print("解析结果:")
    for section, items in result.items():
        print(f"\n[{section}]")
        for key, value in items.items():
            print(f"  {key} = {value} ({type(value).__name__})")