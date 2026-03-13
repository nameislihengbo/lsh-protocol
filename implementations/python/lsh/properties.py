"""
LSH Protocol Property Definition System

提供统一的属性配置框架，用于：
- 详情展示
- 编辑对话框
- 属性验证

设计原则：
- 框架层只提供 PropertyType 和 PropertyDefinition 类
- 具体属性定义由各业务模块的 category_config.py 提供
- 支持动态注册和查询

使用方式：
    from lsh import PropertyType, PropertyDefinition, register_property_definitions
    
    # 业务模块注册属性定义
    register_property_definitions("device", {
        "base_properties": [
            PropertyDefinition("name", "名称", PropertyType.TEXT, required=True),
            ...
        ],
        "extra_properties": [...],
        "display_order": ["name", ...]
    })
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class PropertyType(Enum):
    """属性类型"""
    TEXT = "text"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    SELECT = "select"
    COORDINATES = "coordinates"
    DATE = "date"
    COLOR = "color"
    FILE_PATH = "file_path"


@dataclass
class PropertyDefinition:
    """属性定义"""
    key: str
    display_name: str
    property_type: PropertyType = PropertyType.TEXT
    editable: bool = True
    visible: bool = True
    required: bool = False
    default: Any = None
    default_today: bool = False
    placeholder: str = ""
    tooltip: str = ""
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    options: List[Tuple[str, str]] = field(default_factory=list)
    unit: str = ""
    decimal_places: int = 2


ELEMENT_PROPERTY_DEFINITIONS: Dict[str, Dict[str, Any]] = {}


def register_property_definitions(category: str, definitions: Dict[str, Any]) -> None:
    """注册元素类型的属性定义
    
    Args:
        category: 元素类型
        definitions: 属性定义字典，包含：
            - base_properties: 基础属性列表
            - extra_properties: 扩展属性列表
            - position_properties: 位置属性列表
            - display_order: 展示顺序
    """
    ELEMENT_PROPERTY_DEFINITIONS[category] = definitions


def get_property_definition(category: str) -> Dict[str, Any]:
    """获取元素类型的属性定义
    
    Args:
        category: 元素类型
        
    Returns:
        属性定义字典
    """
    return ELEMENT_PROPERTY_DEFINITIONS.get(category, {})


def get_editable_properties(category: str) -> List[PropertyDefinition]:
    """获取可编辑的属性列表
    
    Args:
        category: 元素类型
        
    Returns:
        可编辑属性定义列表
    """
    definition = get_property_definition(category)
    if not definition:
        return []
    
    editable = []
    for prop_list in [definition.get("base_properties", []),
                      definition.get("extra_properties", []),
                      definition.get("position_properties", [])]:
        for prop in prop_list:
            if prop.editable:
                editable.append(prop)
    
    return editable


def get_display_properties(category: str) -> List[PropertyDefinition]:
    """获取展示的属性列表
    
    Args:
        category: 元素类型
        
    Returns:
        展示属性定义列表（按 display_order 排序）
    """
    definition = get_property_definition(category)
    if not definition:
        return []
    
    all_props = {}
    for prop_list in [definition.get("base_properties", []),
                      definition.get("extra_properties", []),
                      definition.get("position_properties", [])]:
        for prop in prop_list:
            if prop.visible:
                all_props[prop.key] = prop
    
    display_order = definition.get("display_order", [])
    ordered_props = []
    for key in display_order:
        if key in all_props:
            ordered_props.append(all_props[key])
    
    for key, prop in all_props.items():
        if key not in display_order:
            ordered_props.append(prop)
    
    return ordered_props


def get_all_property_definitions() -> Dict[str, Dict[str, Any]]:
    """获取所有属性定义
    
    Returns:
        所有属性定义字典
    """
    return ELEMENT_PROPERTY_DEFINITIONS.copy()
