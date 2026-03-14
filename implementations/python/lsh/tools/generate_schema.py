"""
LSH JSON Schema Generator

从 ELEMENT_PROPERTY_DEFINITIONS 生成 JSON Schema
供 IDE 使用（VS Code, JetBrains 等）

使用方式：
    lsh-schema -o schema.json
    # 或
    python -m lsh.tools.generate_schema
"""

import json
import sys
from pathlib import Path
from typing import Optional

from ..properties import PropertyType, get_all_property_definitions


def generate_json_schema(
    title: str = "LSH Element",
    description: str = "LSH Protocol Element Schema"
) -> dict:
    """生成 JSON Schema
    
    Args:
        title: Schema 标题
        description: Schema 描述
        
    Returns:
        JSON Schema 字典
    """
    definitions = get_all_property_definitions()
    
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": title,
        "description": description,
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "元素唯一标识"
            },
            "name": {
                "type": "string",
                "description": "元素名称"
            },
            "category": {
                "type": "string",
                "description": "元素类型"
            },
            "position": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 3,
                "maxItems": 3,
                "description": "位置坐标 [x, y, z]"
            },
            "size": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 3,
                "maxItems": 3,
                "description": "尺寸 [width, depth, height]"
            },
            "rotation": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 3,
                "maxItems": 3,
                "description": "旋转 [rx, ry, rz]"
            },
            "visible": {
                "type": "boolean",
                "description": "是否可见"
            },
            "state": {
                "type": "string",
                "description": "状态"
            },
        },
        "required": ["id", "name", "category"],
        "definitions": {}
    }
    
    for category, defs in definitions.items():
        cat_schema = _generate_category_schema(category, defs)
        schema["definitions"][category] = cat_schema
        
        schema["properties"][category] = {
            "$ref": f"#/definitions/{category}"
        }
    
    return schema


def _generate_category_schema(category: str, defs: dict) -> dict:
    """生成单个类别的 Schema"""
    props = {}
    required = []
    
    all_props = (
        defs.get("base_properties", []) +
        defs.get("extra_properties", []) +
        defs.get("position_properties", [])
    )
    
    for prop in all_props:
        prop_schema = _property_to_schema(prop)
        props[prop.key] = prop_schema
        
        if prop.required:
            required.append(prop.key)
    
    return {
        "type": "object",
        "properties": props,
        "required": required
    }


def _property_to_schema(prop) -> dict:
    """将 PropertyDefinition 转换为 JSON Schema"""
    result = {
        "description": prop.display_name
    }
    
    if prop.tooltip:
        result["description"] = f"{prop.display_name}: {prop.tooltip}"
    
    prop_type = prop.property_type
    
    if prop_type == PropertyType.TEXT:
        result["type"] = "string"
        if prop.placeholder:
            result["examples"] = [prop.placeholder]
    
    elif prop_type == PropertyType.NUMBER:
        result["type"] = "number"
        if prop.min_value is not None:
            result["minimum"] = prop.min_value
        if prop.max_value is not None:
            result["maximum"] = prop.max_value
        if prop.decimal_places:
            result["multipleOf"] = 10 ** (-prop.decimal_places)
    
    elif prop_type == PropertyType.INTEGER:
        result["type"] = "integer"
        if prop.min_value is not None:
            result["minimum"] = int(prop.min_value)
        if prop.max_value is not None:
            result["maximum"] = int(prop.max_value)
    
    elif prop_type == PropertyType.BOOLEAN:
        result["type"] = "boolean"
    
    elif prop_type == PropertyType.SELECT:
        result["type"] = "string"
        result["enum"] = [v for v, _ in prop.options]
        result["enumNames"] = [d for _, d in prop.options]
    
    elif prop_type == PropertyType.COORDINATES:
        result["type"] = "array"
        result["items"] = {"type": "number"}
        result["minItems"] = 3
        result["maxItems"] = 3
    
    elif prop_type == PropertyType.DATE:
        result["type"] = "string"
        result["format"] = "date-time"
    
    elif prop_type == PropertyType.COLOR:
        result["type"] = "string"
        result["pattern"] = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    
    elif prop_type == PropertyType.FILE_PATH:
        result["type"] = "string"
    
    else:
        result["type"] = "string"
    
    if prop.default is not None:
        result["default"] = prop.default
    
    if prop.unit:
        result["description"] = f"{result['description']} ({prop.unit})"
    
    return result


def main(output_file: Optional[str] = None):
    """主函数
    
    Args:
        output_file: 输出文件路径，None 时输出到 stdout
    """
    schema = generate_json_schema()
    json_str = json.dumps(schema, ensure_ascii=False, indent=2)
    
    if output_file:
        Path(output_file).write_text(json_str, encoding="utf-8")
        print(f"JSON Schema 已生成: {output_file}")
    else:
        print(json_str)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="生成 LSH JSON Schema")
    parser.add_argument("-o", "--output", help="输出文件路径")
    args = parser.parse_args()
    
    main(args.output)
