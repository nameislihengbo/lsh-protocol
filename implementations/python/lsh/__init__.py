"""
LSH Protocol - Python Implementation

LSH 协议 - 虚拟现实交互协议

设计哲学：
- 万物皆元素：一切对象都是元素
- 属性驱动：所有内容都通过属性表达
- 无限扩展：任意属性，无限可能
- 交互同步：发布-订阅模式，交互实时同步到所有端

三要素：
- 元素：一个空白容器
- 关系：ID（系统生成，用于标识）
- 属性：所有内容（name, category, position, size 等）

使用方式：
    from lsh import SceneElement, SceneElementRegistry, view_sync, ViewSyncEvents
    
    # 创建元素（万物皆元素）
    element = SceneElement.create({
        "name": "客厅",
        "category": "room",
        "position": [3, 3, 0],
        "size": [6, 6, 3]
    })
    
    # 属性操作
    element.get_property("name")           # "客厅"
    element.set_property("room_type", "living_room")
    
    # 注册表
    registry = SceneElementRegistry()
    registry.register(element)
    
    # 按属性查找
    registry.find_by_property("category", "room")
    
    # 交互同步
    view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
    view_sync.publish_element_added(element)
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
from .validation import (
    ValidationError,
    ValidationResult,
    validate_element,
    validate_property_value,
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
    "ValidationError",
    "ValidationResult",
    "validate_element",
    "validate_property_value",
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
