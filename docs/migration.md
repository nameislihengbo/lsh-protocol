# 迁移指南：从 v2.x 到 v3.0

本文档帮助你从 LSH 协议 v2.x 迁移到 v3.0.x（含 v3.0.1 代码实现完善）。

## 核心变更

### 1. 移除 ElementType 枚举

v2.x 区分 SPACE/ENTITY 两种类型，v3.0 统一为 Element：

| v2.x | v3.0 | 说明 |
|------|------|------|
| `ElementType.SPACE` | `category="room"` | 通过 category 区分 |
| `ElementType.ENTITY` | `category="device"` | 通过 category 区分 |
| `element.element_type` | `element.category` | 直接访问 category |

### 2. 属性查询机制

v3.0 引入属性查询机制，通过 `get_property()` 获取元素特性：

```python
# v2.x：通过 element_type 判断
if element.element_type == ElementType.SPACE:
    handle_space(element)

# v3.0：通过属性查询
if element.is_space():
    handle_space(element)

# 或使用 get_property
from lsh import get_property
if get_property(element, "can_contain", False):
    handle_container(element)
```

### 3. 方法签名变更

所有 `publish_element_*` 方法的 `element_type: ElementType` 参数改为 `category: str`：

```python
# v2.x
view_sync.publish_element_position_changed(
    "device_001", ElementType.ENTITY, 2.0, 3.0, 1.5
)

# v3.0
view_sync.publish_element_position_changed(
    "device_001", "device", 2.0, 3.0, 1.5
)
```

## 代码迁移示例

### 创建元素

```python
# v2.x
from lsh import SceneElement, ElementType

room = SceneElement.create_space(
    id="room_001",
    name="Living Room",
    position=(0, 0, 0),
    size=(5.0, 4.0, 2.8),
    category="room"
)

# v3.0
from lsh import SceneElement

room = SceneElement.create_room(
    id="room_001",
    name="Living Room",
    position=(0, 0, 0),
    size=(5.0, 4.0, 2.8),
    room_type="living_room"
)
```

### 发布事件

```python
# v2.x
view_sync.publish_element_position_changed(
    "room_001", ElementType.SPACE, 2.0, 3.0, 0
)

# v3.0
view_sync.publish_element_position_changed(
    "room_001", "room", 2.0, 3.0, 0
)
```

### 订阅事件

```python
# v2.x - 通过 target_type 判断
def on_position_changed(event):
    if event.target_type == "space":
        handle_space(event)
    elif event.target_type == "entity":
        handle_entity(event)

# v3.0 - 通过 category 判断
def on_position_changed(event):
    category = event.target_type  # 现在存储 category
    if category == "room":
        handle_room(event)
    elif category == "device":
        handle_device(event)
```

### 搜索元素

```python
# v2.x - 按类型搜索
spaces = registry.get_by_type(ElementType.SPACE)
entities = registry.get_by_type(ElementType.ENTITY)

# v3.0 - 按分类搜索
rooms = registry.get_by_category("room")
devices = registry.get_by_category("device")
```

## CATEGORY_DEFAULTS 配置

v3.0 引入 `CATEGORY_DEFAULTS` 配置，定义各类别的默认属性：

```python
from lsh import CATEGORY_DEFAULTS, get_property

# 默认配置
CATEGORY_DEFAULTS = {
    "room": {"is_space": True},
    "device": {"is_toggleable": True},
    "furniture": {},
    "item": {},
    "door": {},
    "window": {},
    "robot": {"is_movable": True},
    "custom_model": {"is_custom_model": True},
}

# 获取属性
element = SceneElement.create_room(...)
is_space = get_property(element, "is_space", False)  # True
```

## 常见问题

### Q: 为什么要移除 ElementType？

A: "万物皆元素"，SPACE/ENTITY 的区分是冗余的。元素的行为差异通过属性表达，而非类型。

### Q: 如何判断元素是否可包含子元素？

A: v3.0 中"万物皆可包含"，虚拟元素包含信息，实体元素有空间。如需特定判断：

```python
# 通过 is_space 属性判断
if element.is_space():
    # 有边界的空间元素
    pass

# 通过自定义属性判断
if element.get_extra_property("can_contain_children", True):
    pass
```

### Q: 批量模式有变化吗？

A: 没有，批量模式的用法保持不变：

```python
view_sync.batch_begin()
view_sync.publish_element_position_changed("device_001", "device", 1.0, 1.0, 0)
view_sync.publish_element_position_changed("device_002", "device", 2.0, 2.0, 0)
view_sync.batch_end()
```

## 兼容性矩阵

| 功能 | v2.x | v3.0 |
|------|------|------|
| 发布-订阅 | ✅ | ✅ |
| 批量模式 | ✅ | ✅ |
| 位置优先 | ✅ | ✅ |
| 元素注册表 | ✅ | ✅ |
| ElementType 枚举 | ✅ | ❌ |
| category 分类 | ✅ | ✅ |
| 属性查询机制 | ❌ | ✅ |
| CATEGORY_DEFAULTS | ❌ | ✅ |

## 获取帮助

如果你在迁移过程中遇到问题，可以：

1. 查看 [SPEC.md](SPEC.md) 了解完整的协议规范
2. 查看 [examples/python/basic_usage.py](../examples/python/basic_usage.py) 了解基本用法
3. 提交 Issue 到 GitHub 仓库
