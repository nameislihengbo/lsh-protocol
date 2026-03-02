# LSH 视图同步协议

**Li Shi Hang View Synchronization Protocol**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-repo/lsh-protocol)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

LSH 是一种面向虚拟世界的视图同步协议，定义了空间数据的标准化表示和同步机制。

## 核心特性

- **位置优先**：所有事件携带位置信息，实现多视图自动同步
- **极简类型**：仅 SPACE（空间）和 ENTITY（实体）两种核心类型
- **灵活扩展**：通过 `category` 字段实现业务分类，不绑定特定领域
- **批量优化**：支持事件合并，避免重复刷新

## 快速开始

```python
from lsh import SceneElement, ElementType, view_sync, ViewSyncEvents

# 创建空间
room = SceneElement.create_space(
    id="room_001",
    name="客厅",
    size=(5.0, 4.0, 2.8),
    category="room"
)

# 创建实体
device = SceneElement.create_entity(
    id="device_001",
    name="智能灯",
    position=(2.5, 2.0, 1.5),
    category="device",
    parent_id="room_001"
)

# 发布事件
view_sync.publish_element_added(room)
view_sync.publish_element_added(device)

# 订阅事件
def on_element_added(event):
    print(f"元素添加: {event.extra['name']}")

view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
```

## 核心概念

```
┌─────────────────────────────────────────────────────┐
│                    虚拟世界                          │
├─────────────────────────────────────────────────────┤
│  空间        │ 有边界、可包含其他元素        │
│  实体      │ 可交互、有行为               │
│  关系    │ 层级、父子、包含              │
│  属性  │ 位置、旋转、缩放、可见性      │
└─────────────────────────────────────────────────────┘
```

## 文档

- [协议规范 (SPEC.md)](SPEC.md) - 完整的协议定义
- [迁移指南](docs/migration.md) - 从 v1.x 迁移到 v2.0
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
# 克隆仓库
git clone https://github.com/your-repo/lsh-protocol.git

# 安装开发依赖
cd lsh-protocol
pip install -e ".[dev]"

# 运行测试
pytest tests/
```

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 版本历史

| 版本 | 说明 |
|------|------|
| 2.0.0 | 协议重新定位为虚拟世界通用协议；ElementType 简化为 SPACE/ENTITY |
| 1.x | 智能家居领域协议 |
