# 迁移指南：从 v1.x 到 v2.0

本文档帮助你从 LSH 协议 v1.x 迁移到 v2.0.0。

## 核心变更

### 1. ElementType 变更

v1.x 定义了多种业务类型，v2.0 简化为两种核心类型：

| v1.x | v2.0 element_type | v2.0 category |
|------|-------------------|---------------|
| `ROOM` | `SPACE` | `"room"` |
| `DEVICE` | `ENTITY` | `"device"` |
| `ITEM` | `ENTITY` | `"item"` |
| `CUSTOM_MODEL` | `ENTITY` | `"custom_model"` |
| `FURNITURE` | `ENTITY` | `"furniture"` |
| `ROBOT` | `ENTITY` | `"robot"` |
| `MODULE` | `ENTITY` | `"module"` |
| `WALL` | `ENTITY` | `"wall"` |
| `FLOOR_ELEMENT` | `ENTITY` | `"floor_element"` |
| `PATH` | `ENTITY` | `"path"` |

### 2. 事件类型变更

v1.x 有大量领域特定事件，v2.0 统一为 `ELEMENT_*` 事件：

| v1.x | v2.0 |
|------|------|
| `ROOM_ADDED` | `ELEMENT_ADDED` + `category="room"` |
| `ROOM_DELETED` | `ELEMENT_DELETED` + `category="room"` |
| `ROOM_POSITION_CHANGED` | `ELEMENT_POSITION_CHANGED` + `target_type="space"` |
| `ROOM_SIZE_CHANGED` | `ELEMENT_CHANGED` + `category="room"` |
| `DEVICE_ADDED` | `ELEMENT_ADDED` + `category="device"` |
| `DEVICE_DELETED` | `ELEMENT_DELETED` + `category="device"` |
| `DEVICE_POSITION_CHANGED` | `ELEMENT_POSITION_CHANGED` + `target_type="entity"` |
| `DEVICE_STATE_CHANGED` | `ELEMENT_CHANGED` + `category="device"` |
| `DEVICE_ROOM_CHANGED` | `ELEMENT_HIERARCHY_CHANGED` |
| `ITEM_*` | `ELEMENT_*` + `category="item"` |
| `CUSTOM_MODEL_*` | `ELEMENT_*` + `category="custom_model"` |
| `ROBOT_*` | `ELEMENT_*` + `category="robot"` |
| `MODEL_INSTANCE_*` | `ELEMENT_*` + `category="model_instance"` |

## 代码迁移示例

### 创建元素

```python
# v1.x
from src.home3d.models.scene_element import SceneElement, ElementType

element = SceneElement(
    id="device_001",
    name="Smart Light",
    element_type=ElementType.DEVICE,
    position=(2.5, 2.0, 1.5),
    room_id="room_001"
)

# v2.0
from lsh import SceneElement

element = SceneElement.create_entity(
    id="device_001",
    name="Smart Light",
    position=(2.5, 2.0, 1.5),
    category="device",
    parent_id="room_001"
)
```

### 发布事件

```python
# v1.x
view_sync.publish_room_position_changed("room_001", 2.0, 3.0, 0)

# v2.0
from lsh import ElementType
view_sync.publish_element_position_changed("room_001", ElementType.SPACE, 2.0, 3.0, 0)
```

```python
# v1.x
view_sync.publish_device_state_changed("device_001", DeviceState.ON)

# v2.0
element = SceneElement.create_entity(
    id="device_001",
    name="Smart Light",
    category="device",
    extra={"state": "on"}
)
view_sync.publish_element_changed(element)
```

### 订阅事件

```python
# v1.x - 分别订阅不同类型
view_sync.subscribe(ViewSyncEvents.ROOM_POSITION_CHANGED, on_room_moved)
view_sync.subscribe(ViewSyncEvents.DEVICE_POSITION_CHANGED, on_device_moved)

# v2.0 - 统一订阅，按需处理
view_sync.subscribe(ViewSyncEvents.ELEMENT_POSITION_CHANGED, on_position_changed)

def on_position_changed(event):
    target_type = event.target_type  # "space" or "entity"
    category = event.extra.get("category", "")
    
    if target_type == "space":
        handle_space_moved(event)
    elif category == "device":
        handle_device_moved(event)
```

### 搜索元素

```python
# v1.x - 按类型搜索
devices = registry.get_by_type(ElementType.DEVICE)

# v2.0 - 按类型或分类搜索
entities = registry.get_entities()  # 所有实体
devices = registry.get_by_category("device")  # 按分类
```

## 新增功能

### 1. Bounds（边界）

v2.0 新增 `Bounds` 类，用于定义空间边界：

```python
from lsh import SceneElement, Bounds

# 创建空间时自动生成边界
room = SceneElement.create_space(
    id="room_001",
    name="Living Room",
    size=(5.0, 4.0, 2.8),
    category="room"
)

# 边界自动设置
print(room.bounds)  # Bounds(min_x=0, max_x=5, min_y=0, max_y=4, min_z=0, max_z=2.8)

# 检查点是否在边界内
print(room.bounds.contains_point(2.5, 2.0, 1.4))  # True
```

### 2. Tags（标签）

v2.0 支持通过标签进行分类：

```python
element = SceneElement.create_entity(
    id="device_001",
    name="Smart Light",
    category="device",
    tags=["smart", "lighting", "zigbee"]
)

# 按标签搜索
smart_devices = registry.get_by_tag("smart")
```

### 3. 层级策略

v2.0 支持不同的层级跟随策略：

```python
from lsh import HierarchyPolicy

# 跟随父元素移动（默认）
element.hierarchy_policy = HierarchyPolicy.FOLLOW_PARENT

# 固定位置
element.hierarchy_policy = HierarchyPolicy.FIXED

# 独立移动
element.hierarchy_policy = HierarchyPolicy.INDEPENDENT
```

## 常见问题

### Q: 为什么要移除 ROOM/DEVICE 等类型？

A: 这些类型是业务概念，不是协议核心。通过 `category` 字段可以更灵活地支持不同业务场景，同时保持协议的简洁性。

### Q: 如何处理现有代码中的 room_id？

A: v2.0 使用 `parent_id` 表示层级关系，`room_id` 可以存储在 `extra` 字段中：

```python
element = SceneElement.create_entity(
    id="device_001",
    name="Smart Light",
    category="device",
    parent_id="room_001",  # 层级关系
    extra={"room_id": "room_001"}  # 业务字段（可选）
)
```

### Q: 批量模式有变化吗？

A: 没有，批量模式的用法保持不变：

```python
view_sync.batch_begin()
view_sync.publish_element_position_changed("device_001", ElementType.ENTITY, 1.0, 1.0, 0)
view_sync.publish_element_position_changed("device_002", ElementType.ENTITY, 2.0, 2.0, 0)
view_sync.batch_end()  # 合并处理
```

## 兼容性矩阵

| 功能 | v1.x | v2.0 |
|------|------|------|
| 发布-订阅 | ✅ | ✅ |
| 批量模式 | ✅ | ✅ |
| 位置优先 | ✅ | ✅ |
| 元素注册表 | ✅ | ✅ |
| SPACE/ENTITY 类型 | ❌ | ✅ |
| category 分类 | ❌ | ✅ |
| tags 标签 | ❌ | ✅ |
| Bounds 边界 | ❌ | ✅ |
| 层级策略 | ❌ | ✅ |

## 获取帮助

如果你在迁移过程中遇到问题，可以：

1. 查看 [SPEC.md](SPEC.md) 了解完整的协议规范
2. 查看 [examples/python/basic_usage.py](../examples/python/basic_usage.py) 了解基本用法
3. 提交 Issue 到 GitHub 仓库
