"""
LSH Protocol - Python Implementation

LSH 协议 - 万物皆元素，属性驱动，无限扩展

设计哲学：
- 万物皆元素：一切对象都是元素
- 属性驱动：所有内容都通过属性表达
- 无限扩展：任意属性，无限可能

三要素：
- 元素：一个空白容器
- 关系：ID（系统生成，用于标识）
- 属性：所有内容（name, category, position, size 等）

使用方式：
    from lsh import SceneElement, SceneElementRegistry
    
    # 创建空白元素
    element = SceneElement.create()
    
    # 创建沙发
    sofa = SceneElement.create({
        "name": "沙发",
        "category": "furniture",
        "position": [4, 3, 0],
        "size": [2.5, 1, 0.8],
        "eng_name": "sofa"
    })
    
    # 属性操作
    sofa.get_property("name")           # "沙发"
    sofa.set_property("color", "red")   # 设置颜色
    
    # 注册表
    registry = SceneElementRegistry()
    registry.register(sofa)
    registry.find_by_property("category", "furniture")
    registry.find_by_property("name", "沙发")
"""

from .core import (
    SceneElement,
    SceneElementRegistry,
)
from .sync import (
    ViewSyncEvents,
    PositionData,
    SizeData,
    ViewSyncEvent,
    ViewSyncManager,
    view_sync,
    LSH_PROTOCOL_VERSION,
)
from .properties import (
    PropertyType,
    PropertyDefinition,
    ELEMENT_PROPERTY_DEFINITIONS,
    register_property_definitions,
    get_property_definition,
    get_editable_properties,
    get_display_properties,
    get_all_property_definitions,
)
from .coord import (
    lsh_to_godot_position,
    lsh_to_godot_size,
    lsh_to_godot_rotation,
    lsh_to_godot_bounds,
    godot_to_lsh_position,
    godot_to_lsh_bounds,
    lsh_to_vtk_position,
    lsh_to_vtk_size,
    lsh_to_vtk_rotation,
    lsh_to_vtk_bounds,
    vtk_to_lsh_position,
    vtk_to_lsh_bounds,
)

__version__ = "3.1.0"
__author__ = "Li Hengbo"
__license__ = "MIT"

__all__ = [
    "SceneElement",
    "SceneElementRegistry",
    "ViewSyncEvents",
    "PositionData",
    "SizeData",
    "ViewSyncEvent",
    "ViewSyncManager",
    "view_sync",
    "LSH_PROTOCOL_VERSION",
    "PropertyType",
    "PropertyDefinition",
    "ELEMENT_PROPERTY_DEFINITIONS",
    "register_property_definitions",
    "get_property_definition",
    "get_editable_properties",
    "get_display_properties",
    "get_all_property_definitions",
    "lsh_to_godot_position",
    "lsh_to_godot_size",
    "lsh_to_godot_rotation",
    "lsh_to_godot_bounds",
    "godot_to_lsh_position",
    "godot_to_lsh_bounds",
    "lsh_to_vtk_position",
    "lsh_to_vtk_size",
    "lsh_to_vtk_rotation",
    "lsh_to_vtk_bounds",
    "vtk_to_lsh_position",
    "vtk_to_lsh_bounds",
]
