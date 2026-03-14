"""
LSH VS Code Snippets Generator

从 ELEMENT_TYPES 生成 VS Code Snippets
提供代码补全支持

使用方式：
    lsh-snippets -o lsh.code-snippets
    # 或
    python -m lsh.tools.generate_snippets
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def generate_snippets() -> Dict[str, Any]:
    """生成 VS Code Snippets
    
    Returns:
        Snippets 字典
    """
    snippets = {}
    
    snippets.update(_generate_element_snippets())
    snippets.update(_generate_property_snippets())
    snippets.update(_generate_command_snippets())
    
    return snippets


def _generate_element_snippets() -> Dict[str, Any]:
    """生成元素创建 Snippets"""
    snippets = {}
    
    element_types = {
        "home": {"display_name": "家", "is_space": True},
        "floor": {"display_name": "楼层", "is_space": True},
        "room": {"display_name": "房间", "is_space": True},
        "device": {"display_name": "设备", "is_toggleable": True},
        "light": {"display_name": "灯", "is_toggleable": True, "default_size": (0.1, 0.1, 0.1)},
        "ac": {"display_name": "空调", "is_toggleable": True, "default_size": (0.8, 0.3, 0.2)},
        "tv": {"display_name": "电视", "is_toggleable": True, "default_size": (1.2, 0.05, 0.7)},
        "furniture": {"display_name": "家具"},
        "sofa": {"display_name": "沙发", "default_size": (2.0, 0.8, 0.8)},
        "bed": {"display_name": "床", "default_size": (2.0, 1.8, 0.5)},
        "item": {"display_name": "物品"},
        "food": {"display_name": "食品"},
        "robot": {"display_name": "机器人", "is_movable": True},
    }
    
    for category, config in element_types.items():
        display_name = config.get("display_name", category)
        body_parts = [
            '"${1:id}:${2:' + display_name + '}:${3:@${4:0,0,0}}:${5:${6:container}}:type=' + category
        ]
        
        if config.get("is_toggleable"):
            body_parts[0] += ',s=${7:off}'
        
        if config.get("default_size"):
            size = config["default_size"]
            body_parts[0] += f',size={size[0]},{size[1]},{size[2]}'
        
        body_parts[0] += '"'
        
        snippets[category] = {
            "prefix": category,
            "body": body_parts,
            "description": f"创建 {display_name} 元素",
            "scope": "lsh"
        }
    
    return snippets


def _generate_property_snippets() -> Dict[str, Any]:
    """生成属性 Snippets"""
    snippets = {}
    
    property_templates = {
        "position": {
            "prefix": "pos",
            "body": ['"${1:id}:s=${2:off}:@${3:0,0,0}"'],
            "description": "更新元素位置"
        },
        "state": {
            "prefix": "state",
            "body": ['"${1:id}:s=${2|off,on|}"'],
            "description": "更新元素状态"
        },
        "temperature": {
            "prefix": "temp",
            "body": ['"${1:id}:t=${2:24}"'],
            "description": "设置温度"
        },
        "brightness": {
            "prefix": "bright",
            "body": ['"${1:id}:brightness=${2:100}"'],
            "description": "设置亮度"
        },
        "battery": {
            "prefix": "bat",
            "body": ['"${1:id}:bat=${2:80}"'],
            "description": "设置电量"
        },
    }
    
    snippets.update(property_templates)
    
    return snippets


def _generate_command_snippets() -> Dict[str, Any]:
    """生成命令 Snippets"""
    snippets = {}
    
    command_templates = {
        "lsh_element": {
            "prefix": "lsh",
            "body": [
                '"${1:id}:${2:name}:@${3:0,0,0}:${4:container}:type=${5:category},${6:props}"'
            ],
            "description": "创建 LSH 元素"
        },
        "lsh_update": {
            "prefix": "lsh-update",
            "body": ['"${1:id}:${2:prop}=${3:value}"'],
            "description": "更新元素属性"
        },
        "lsh_batch": {
            "prefix": "lsh-batch",
            "body": [
                '"${1:id1}:${2:prop1}=${3:value1}"',
                '"${4:id2}:${5:prop2}=${6:value2}"',
            ],
            "description": "批量更新元素"
        },
    }
    
    snippets.update(command_templates)
    
    return snippets


def main(output_file: Optional[str] = None):
    """主函数
    
    Args:
        output_file: 输出文件路径，None 时输出到 stdout
    """
    snippets = generate_snippets()
    json_str = json.dumps(snippets, ensure_ascii=False, indent=2)
    
    if output_file:
        Path(output_file).write_text(json_str, encoding="utf-8")
        print(f"VS Code Snippets 已生成: {output_file}")
    else:
        print(json_str)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="生成 LSH VS Code Snippets")
    parser.add_argument("-o", "--output", help="输出文件路径")
    args = parser.parse_args()
    
    main(args.output)
