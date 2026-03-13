# LSH 视图同步协议

**Li Shi Hang View Synchronization Protocol**

[![Version](https://img.shields.io/badge/version-3.1.1-blue.svg)](https://github.com/your-repo/lsh-protocol)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

LSH 是一种**虚拟现实统一协议**，定义了场景数据的标准化表示和同步机制。无论是虚拟世界还是现实世界，都可以被抽象为**元素、关系、属性**三要素。

## 核心特性

- **分层架构**：Model/ActorFactory/View 三层分离，数据与渲染彻底解耦
- **位置优先**：所有事件携带位置信息，实现多视图自动同步
- **万物皆元素**：统一元素模型，通过属性区分行为
- **灵活扩展**：通过 `category` 字段实现业务分类，不绑定特定领域
- **批量优化**：支持事件合并，避免重复刷新
- **坐标系分离**：对外统一使用 LSH 坐标系，内部渲染层透明转换

## v3.1.1 架构改造完成

本次版本完成了 Home3D/Multimodal/Robot 三大模块的 LSH 协议统一改造：

### 改造统计

| 指标 | 数量 |
|------|------|
| **总文件变更** | 387 个文件 |
| **删除文件** | 142 个 |
| **新增文件** | 145 个 |
| **修改文件** | 99 个 |
| **代码行变化** | +50,815 / -79,403（净减少 28,588 行） |

### 核心变化

| 改造前 | 改造后 |
|--------|--------|
| 各模块独立实现元素模型 | 统一 `lsh-protocol` 子模块 |
| 重复的 `scene_element.py` | 统一 `lsh.core.SceneElement` |
| 重复的 `view_sync.py` | 统一 `lsh.sync.ViewSyncManager` |
| 重复的 `coord_transform.py` | 统一 `lsh.coord.*` 坐标转换 |
| 无属性定义系统 | 新增 `lsh.properties` 属性定义框架 |
| ElementType 枚举硬编码 | category 字符串 + 配置 |
| 修改核心代码扩展 | 注册新 category 即可 |

### 三大模块统一

| 模块 | 元素类型 | 说明 |
|------|----------|------|
| **Home3D** | room, device, furniture, item, sensor, door, window | 空间与实体 |
| **Multimodal** | ai_model, ai_conversation, ai_message, knowledge_base | AI 智能体 |
| **Robot** | robot, robot_task, robot_experience, robot_servo | 具身智能 |

### 导入方式变化

```python
# 改造前（各模块独立导入）
from src.home3d.models.scene_element import SceneElement
from src.home3d.view_sync import view_sync, ViewSyncEvents
from src.home3d.utils.coord_transform import lsh_to_vtk_position

# 改造后（统一从 LSH 导入）
from lsh import SceneElement, view_sync, ViewSyncEvents
from lsh import lsh_to_vtk_position, lsh_to_godot_position
```

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

# 创建元素（万物皆元素，通过 category 区分）
element = SceneElement(
    id="unique_id",
    name="显示名称",
    category="device",  # 决定行为，而非类型
    position=[x, y, z],
    size=[w, d, h],
    extra={
        # 所有扩展属性存储在这里
        "state": "on",
        "power_consumption": 15.0,
    }
)

# 发布事件
view_sync.publish_element_added(element)

# 订阅事件
def on_element_added(event):
    print(f"元素添加: {event.extra['name']}")

view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
```

## 核心概念

```
┌─────────────────────────────────────────────────────┐
│              虚拟世界 / 现实世界                      │
├─────────────────────────────────────────────────────┤
│  元素 (Element)  │ 一切对象（虚拟/实体）        │
│  关系 (Relation) │ 层级、父子、包含              │
│  属性 (Property) │ 位置、旋转、缩放、可见性      │
└─────────────────────────────────────────────────────┘
```

**万物皆元素**：场景中的所有对象都是元素，通过属性区分行为。

| category | 说明 | 默认属性 |
|----------|------|----------|
| `room` | 房间 | is_space=True |
| `device` | 设备 | is_toggleable=True |
| `furniture` | 家具 | - |
| `item` | 物品 | - |
| `ai_model` | AI 模型 | is_ai=True, is_virtual=True |
| `robot` | 机器人 | is_movable=True, is_ai=True |
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
| 具身智能 | AI 模型、机器人与空间的统一管理 |

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
| 3.1.1 | 架构改造完成：三模块统一、删除冗余文件、引擎模式统一、净减少 28,588 行代码 |
| 3.0.1 | 代码实现完善：移除 ElementType 枚举；添加便捷方法；完善 CATEGORY_DEFAULTS |
| 3.0.0 | 核心概念简化：移除 SPACE/ENTITY 区分，统一为 Element；属性查询机制 |
| 2.6.0 | 事件溯源架构：定义事件溯源接口，支持时间旅行和状态回滚 |
| 2.5.0 | 分层架构设计：Model/ActorFactory/View 三层分离，数据与渲染彻底解耦 |
| 2.4.0 | 内外坐标系分离架构：明确"输入/输出使用LSH、内部渲染层转换"原则 |
| 2.3.0 | 3D 引擎坐标转换规范：定义 LSH/Godot/VTK/Blender 坐标系转换规则 |
| 2.0.0 | 协议重新定位为虚拟世界通用协议；ElementType 简化为 SPACE/ENTITY |
| 1.x | 智能家居领域协议 |
