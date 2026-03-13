"""
LSH Protocol - Python Implementation

Li Shi Hang Protocol v3.1.0
虚拟现实统一协议 - 虚拟世界和现实世界的统一抽象

设计哲学：
- 万物互联：任何元素可以与任何元素建立关系
- 属性驱动：行为由属性决定，不依赖类型判断
- 无限扩展：注册新 category，建立新关系，无需修改核心代码

核心概念：
- 元素（Element）：万物皆元素，差异通过属性表达
- 关系（Relation）：层级、父子、包含
- 属性（Property）：位置、旋转、缩放、可见性

使用方式：
    from lsh import SceneElement, view_sync, ViewSyncEvents
    
    # 创建元素
    room = SceneElement.create(
        id="room_001", 
        name="客厅", 
        category="room",
        size=(5.0, 4.0, 2.8),
    )
    
    # 发布事件
    view_sync.publish_element_added(room)
    
    # 订阅事件
    view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, callback)
"""

from .core import (
    HierarchyPolicy,
    Bounds,
    CATEGORY_DEFAULTS,
    register_category,
    get_category_config,
    get_category_property,
    get_all_categories,
    get_categories_by_property,
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
    "HierarchyPolicy",
    "Bounds",
    "CATEGORY_DEFAULTS",
    "register_category",
    "get_category_config",
    "get_category_property",
    "get_all_categories",
    "get_categories_by_property",
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
