"""
LSH TypeScript Generator

从 ELEMENT_PROPERTY_DEFINITIONS 生成 TypeScript 类型定义
供前端开发使用

使用方式：
    lsh-typescript -o lsh-types.ts
    # 或
    python -m lsh.tools.generate_typescript
"""

import sys
from pathlib import Path
from typing import Optional

from ..properties import PropertyType, get_all_property_definitions


def generate_typescript(
    namespace: str = "LSH"
) -> str:
    """生成 TypeScript 类型定义
    
    Args:
        namespace: 命名空间
        
    Returns:
        TypeScript 代码字符串
    """
    definitions = get_all_property_definitions()
    
    lines = [
        "/**",
        " * LSH Protocol TypeScript Types",
        " * Auto-generated from ELEMENT_PROPERTY_DEFINITIONS",
        " * Do not edit manually",
        " */",
        "",
        f"export namespace {namespace} {{",
        "",
    ]
    
    lines.extend(_generate_base_types())
    
    for category, defs in definitions.items():
        lines.extend(_generate_category_type(category, defs))
    
    lines.extend(_generate_union_types(definitions))
    
    lines.append("}")
    
    return "\n".join(lines)


def _generate_base_types() -> list:
    """生成基础类型"""
    return [
        "  /** 基础元素接口 */",
        "  interface BaseElement {",
        "    /** 元素唯一标识 */",
        "    id: string;",
        "    /** 元素名称 */",
        "    name: string;",
        "    /** 元素类型 */",
        "    category: string;",
        "    /** 位置坐标 [x, y, z] */",
        "    position?: [number, number, number];",
        "    /** 尺寸 [width, depth, height] */",
        "    size?: [number, number, number];",
        "    /** 旋转 [rx, ry, rz] */",
        "    rotation?: [number, number, number];",
        "    /** 是否可见 */",
        "    visible?: boolean;",
        "    /** 父元素 ID */",
        "    parent_id?: string;",
        "    /** 创建时间 */",
        "    created_at?: string;",
        "    /** 更新时间 */",
        "    updated_at?: string;",
        "  }",
        "",
        "  /** 属性类型枚举 */",
        "  enum PropertyType {",
        "    TEXT = 'text',",
        "    NUMBER = 'number',",
        "    INTEGER = 'integer',",
        "    BOOLEAN = 'boolean',",
        "    SELECT = 'select',",
        "    COORDINATES = 'coordinates',",
        "    DATE = 'date',",
        "    COLOR = 'color',",
        "    FILE_PATH = 'file_path',",
        "  }",
        "",
    ]


def _generate_category_type(category: str, defs: dict) -> list:
    """生成单个类别的类型定义"""
    class_name = _to_pascal_case(category)
    
    lines = [
        f"  /** {category} 元素 */",
        f"  interface {class_name}Element extends BaseElement {{",
    ]
    
    all_props = (
        defs.get("base_properties", []) +
        defs.get("extra_properties", []) +
        defs.get("position_properties", [])
    )
    
    for prop in all_props:
        ts_type = _property_to_typescript(prop)
        optional = "" if prop.required else "?"
        comment = prop.display_name
        if prop.unit:
            comment += f" ({prop.unit})"
        if prop.tooltip:
            comment += f" - {prop.tooltip}"
        
        lines.append(f"    /** {comment} */")
        lines.append(f"    {prop.key}{optional}: {ts_type};")
    
    lines.append("  }")
    lines.append("")
    
    return lines


def _property_to_typescript(prop) -> str:
    """将 PropertyDefinition 转换为 TypeScript 类型"""
    prop_type = prop.property_type
    
    type_map = {
        PropertyType.TEXT: "string",
        PropertyType.NUMBER: "number",
        PropertyType.INTEGER: "number",
        PropertyType.BOOLEAN: "boolean",
        PropertyType.SELECT: "string",
        PropertyType.COORDINATES: "[number, number, number]",
        PropertyType.DATE: "string",
        PropertyType.COLOR: "string",
        PropertyType.FILE_PATH: "string",
    }
    
    ts_type = type_map.get(prop_type, "any")
    
    if prop.property_type == PropertyType.SELECT and prop.options:
        values = " | ".join(f'"{v}"' for v, _ in prop.options)
        ts_type = values
    
    return ts_type


def _generate_union_types(definitions: dict) -> list:
    """生成联合类型"""
    categories = list(definitions.keys())
    
    lines = [
        "  /** 所有元素类型联合 */",
        "  type Element =",
    ]
    
    type_names = [_to_pascal_case(c) + "Element" for c in categories]
    
    for i, name in enumerate(type_names):
        if i < len(type_names) - 1:
            lines.append(f"    | {name}")
        else:
            lines.append(f"    | {name};")
    
    lines.extend([
        "",
        "  /** 所有元素类型 */",
        "  type Category =",
    ])
    
    for i, cat in enumerate(categories):
        if i < len(categories) - 1:
            lines.append(f'    | "{cat}"')
        else:
            lines.append(f'    | "{cat}";')
    
    lines.append("")
    
    return lines


def _to_pascal_case(s: str) -> str:
    """转换为 PascalCase"""
    parts = s.split("_")
    return "".join(p.capitalize() for p in parts)


def main(output_file: Optional[str] = None):
    """主函数
    
    Args:
        output_file: 输出文件路径，None 时输出到 stdout
    """
    ts_code = generate_typescript()
    
    if output_file:
        Path(output_file).write_text(ts_code, encoding="utf-8")
        print(f"TypeScript 类型已生成: {output_file}")
    else:
        print(ts_code)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="生成 LSH TypeScript 类型")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-n", "--namespace", default="LSH", help="命名空间")
    args = parser.parse_args()
    
    main(args.output)
