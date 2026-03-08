# LSH 视图同步协议

**Li Shi Hang View Synchronization Protocol**

[![Version](https://img.shields.io/badge/version-3.0.1-blue.svg)](https://github.com/your-repo/lsh-protocol)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

LSH 是一种**虚拟与现实对接协议**，定义了场景数据的标准化表示和同步机制。无论是虚拟世界还是现实世界，都可以被抽象为**元素、关系、属性**三要素。

## 核心特性

- **分层架构**：Model/ActorFactory/View 三层分离，数据与渲染彻底解耦
- **位置优先**：所有事件携带位置信息，实现多视图自动同步
- **万物皆元素**：统一元素模型，通过属性区分行为
- **灵活扩展**：通过 `category` 字段实现业务分类，不绑定特定领域
- **批量优化**：支持事件合并，避免重复刷新
- **坐标系分离**：对外统一使用 LSH 坐标系，内部渲染层透明转换

## 坐标系

LSH 协议采用建筑/BIM 风格的右手坐标系：

```
Z ↑ (高度/height)
  │
  │     ┌─────────┐
  │     │  元素   │
  │     │Element  │
  │     └─────────┘
  │
  └──────────────────────→ X (宽度/width)
Y (深度/depth，向前)
```

| 轴 | 方向 | 说明 | 对应尺寸 |
|----|------|------|----------|
| X | 向右 | 水平方向 | width (宽度) |
| Y | 向前 | 深度方向 | depth (深度) |
| Z | 向上 | 高度方向 | height (高度) |

### 内外坐标系分离架构

```
┌─────────────────────────────────────────────────────────────┐
│                 外部接口层 (LSH)                             │
│  • 数据输入/输出：全部使用 LSH 坐标系                        │
│  • API 参数：position=(x, y, z) = (右, 前, 上)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              坐标转换层 (适配器)                             │
│  • LSH → 引擎坐标：渲染前转换                               │
│  • 引擎 → LSH：返回数据转换                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              内部渲染层 (引擎坐标)                           │
│  • VTK: X=右, Y=上, Z=前                                    │
│  • Godot: X=右, Y=上, Z=后                                  │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

```python
from lsh import SceneElement, view_sync, ViewSyncEvents

room = SceneElement.create_room(
    id="room_001",
    name="客厅",
    position=(0, 0, 0),        
    size=(5.0, 4.0, 2.8),      
    room_type="living_room"
)

device = SceneElement.create_device(
    id="device_001",
    name="智能灯",
    position=(2.5, 2.0, 1.5),  
    device_type="light",
    parent_id="room_001"
)

view_sync.publish_element_added(room)
view_sync.publish_element_added(device)

def on_element_added(event):
    print(f"元素添加: {event.extra['name']}")

view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
```

## 核心概念

```
┌─────────────────────────────────────────────────────┐
│              虚拟世界 / 现实世界                      │
├─────────────────────────────────────────────────────┤
│  元素    │ 一切对象（虚拟/实体）        │
│  关系   │ 层级、父子、包含              │
│  属性  │ 位置、旋转、缩放、可见性      │
└─────────────────────────────────────────────────────┘
```

**万物皆元素**：场景中的所有对象都是元素，通过属性区分行为。

| category | 说明 | 默认属性 |
|----------|------|----------|
| `room` | 房间 | is_space=True |
| `device` | 设备 | is_toggleable=True |
| `furniture` | 家具 | - |
| `item` | 物品 | - |
| `...` | 用户自定义 | 自定义 |

## 文档

- [协议规范 (SPEC.md)](SPEC.md) - 完整的协议定义
- [迁移指南](docs/migration.md) - 从 v2.x 迁移到 v3.0
- [API 参考](docs/api.md) - 详细的 API 文档

## 应用场景

| 场景 | 说明 |
|------|------|
| 智能家居 | 房间、设备、物品的可视化管理 |
| 数字孪生 | 工厂、建筑的实时监控 |
| 游戏引擎 | 场景编辑器、关卡设计 |
| 元宇宙 | 虚拟空间的多视图同步 |

## 安装

```bash
pip install lsh-protocol
```

## 开发

```bash
git clone https://github.com/your-repo/lsh-protocol.git

cd lsh-protocol
pip install -e ".[dev]"

pytest tests/
```

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 版本历史

| 版本 | 说明 |
|------|------|
| 3.0.1 | 代码实现完善：移除 ElementType 枚举；添加便捷方法；完善 CATEGORY_DEFAULTS |
| 3.0.0 | 核心概念简化：移除 SPACE/ENTITY 区分，统一为 Element；属性查询机制 |
| 2.6.0 | 事件溯源架构：定义事件溯源接口，支持时间旅行和状态回滚 |
| 2.5.0 | 分层架构设计：Model/ActorFactory/View 三层分离，数据与渲染彻底解耦 |
| 2.4.0 | 内外坐标系分离架构：明确"输入/输出使用LSH、内部渲染层转换"原则 |
| 2.3.0 | 3D 引擎坐标转换规范：定义 LSH/Godot/VTK/Blender 坐标系转换规则 |
| 2.0.0 | 协议重新定位为虚拟世界通用协议；ElementType 简化为 SPACE/ENTITY |
| 1.x | 智能家居领域协议 |
