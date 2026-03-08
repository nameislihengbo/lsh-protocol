# LSH 协议

**Li Shi Hang Protocol - 虚拟现实统一协议**

| 属性   | 值                 |
| ------ | ------------------ |
| 版本   | 3.0.2              |
| 状态   | 正式版 (Release)   |
| 作者   | 李恒波 (Li Hengbo) |
| 日期   | 2026-03-08         |
| 许可证 | MIT                |

---

## 1. 摘要 (Abstract)

LSH 协议是一种**虚拟现实统一协议**，将虚拟世界和现实世界统一抽象为**元素、关系、属性**三要素，实现统一的建模、交互和同步。

**核心能力**：

| 能力 | 说明 |
|------|------|
| **统一建模** | 虚拟/现实对象统一为元素模型 |
| **视图同步** | 多视图数据一致性（v2.0 核心能力） |
| **交互协议** | 标准化的用户交互规范 |
| **坐标系统** | 统一的空间坐标定义 |
| **事件驱动** | 发布-订阅模式的状态同步 |

**v3.0.0 重大更新**：

- **协议重新定位**：从"视图同步协议"升级为"虚拟现实统一协议"
- **核心概念简化**：从四要素简化为三要素（元素、关系、属性）
- **移除类型约束**：不再区分 SPACE/ENTITY，统一为 Element
- **属性查询机制**：通过 category 默认配置 + extra 覆盖实现灵活扩展

---

## 2. 应用场景

**应用场景**：

| 场景层级       | 说明               | 典型应用                       |
| -------------- | ------------------ | ------------------------------ |
| **家庭** | 智能家居、物品管理 | 房间、设备、家具的可视化管理   |
| **社区** | 社区管理与服务     | 门禁、停车、公共设施、环境监测 |
| **城市** | 城市级应用         | 交通管理、城市安防、公共服务   |
| **国家** | 跨区域协调         | 物流网络、能源调度、应急响应   |
| **世界** | 全球虚拟世界       | 元宇宙、跨国协作、全球模拟     |

**场景延伸路线**：家庭 → 社区 → 城市 → 国家 → 世界

---

## 3. 核心概念 (Core Concepts)

### 3.1 设计哲学

LSH 协议遵循三大核心设计理念：

| 理念 | 说明 |
|------|------|
| **万物互联** | 任何元素可以与任何元素建立关系，通过 `parent_id`/`children_ids`/`extra.ref_*` 实现灵活连接 |
| **属性驱动** | 行为由属性决定，不依赖类型判断。通过 `get_property()` 查询，支持 category 默认值 + extra 覆盖 |
| **无限扩展** | 注册新 category，建立新关系，无需修改核心代码。系统通过 `register_category()` 动态扩展 |

### 3.2 虚拟现实对应

LSH 协议的核心价值在于建立虚拟世界与现实世界的统一映射：

```
┌─────────────────────────────────────────────────────────────────┐
│                    虚拟现实对应关系                              │
├─────────────────────────────────────────────────────────────────┤
│  现实世界              虚拟世界              对应方式            │
├─────────────────────────────────────────────────────────────────┤
│  物理设备（灯、空调）  →  虚拟元素（device）  →  id 绑定         │
│  物理空间（房间）      →  虚拟元素（room）    →  id 绑定         │
│  传感器数据            →  extra.sensor_*     →  属性映射         │
│  设备状态              →  extra.state        →  属性同步         │
│  用户操作              →  事件触发            →  双向通信         │
└─────────────────────────────────────────────────────────────────┘
```

**对应机制**：

| 机制 | 说明 | 示例 |
|------|------|------|
| **ID 绑定** | 虚拟元素 ID 与现实设备 ID 一一对应 | `device_001` → 现实中的智能灯 |
| **属性映射** | 现实状态映射到虚拟属性 | `extra.state="on"` 表示灯亮 |
| **事件同步** | 现实变化触发虚拟事件，虚拟操作驱动现实变化 | 设备状态变化 → `ELEMENT_CHANGED` |
| **双向通信** | 虚拟操作 → 现实执行，现实变化 → 虚拟更新 | 点击开关 → 设备响应 → 状态回传 |

**扩展属性约定**：

```python
# 现实设备绑定
extra = {
    "real_device_id": "zigbee_001",      # 现实设备标识
    "real_device_type": "zigbee_light",  # 现实设备类型
    "state": "on",                        # 设备状态
    "online": True,                       # 在线状态
}

# 传感器数据
extra = {
    "sensor_type": "temperature",         # 传感器类型
    "sensor_value": 25.5,                 # 当前值
    "sensor_unit": "°C",                  # 单位
    "last_update": "2026-03-08T10:30:00", # 最后更新时间
}
```

### 3.4 三要素抽象

LSH 协议将虚拟世界和现实世界统一抽象为三个核心要素：

```
┌─────────────────────────────────────────────────────┐
│              虚拟世界 / 现实世界                      │
├─────────────────────────────────────────────────────┤
│  元素    │ 一切对象（虚拟/实体）        │
│  关系   │ 元素之间的连接（层级、引用）    │
│  属性  │ 元素的特性（位置、状态、扩展）  │
└─────────────────────────────────────────────────────┘
```

### 3.5 元素 (Element)

**一切皆元素**：场景中的所有对象都是元素，通过属性区分行为。

| 属性 | 类型 | 说明 |
|------|------|------|
| `id` | str | 唯一标识 |
| `name` | str | 元素名称 |
| `category` | str | 业务分类（room, device, furniture 等） |
| `position` | List[float] | 位置 (x, y, z) |
| `size` | List[float] | 尺寸 (width, depth, height) |
| `rotation` | List[float] | 旋转 (rx, ry, rz) |
| `parent_id` | str | 父元素 ID |
| `children_ids` | List[str] | 子元素 ID 列表 |
| `visible` | bool | 是否可见 |
| `extra` | Dict | 自定义属性 |

### 3.6 关系 (Relation)

元素之间的关系通过 ID 引用表达：

| 关系类型 | 属性 | 说明 |
|----------|------|------|
| 层级关系 | `parent_id` | 父元素 ID |
| 包含关系 | `children_ids` | 子元素 ID 列表 |
| 引用关系 | `extra.ref_*` | 其他引用 |

### 3.7 属性 (Property)

属性描述元素的所有特性：

| 属性类别 | 属性 | 说明 |
|----------|------|------|
| **基础** | `id`, `name`, `category` | 标识和分类 |
| **空间** | `position`, `size`, `rotation` | 空间变换 |
| **关系** | `parent_id`, `children_ids` | 层级关系 |
| **状态** | `visible` | 运行状态 |
| **扩展** | `extra` | 自定义属性 |

### 3.8 属性查询机制

**默认值 + 覆盖机制**：

```python
# category 默认配置
CATEGORY_DEFAULTS = {
    "room": {"is_space": True},
    "device": {"is_toggleable": True},
    "furniture": {},
    "item": {},
    "door": {},
    "window": {},
    "robot": {"is_movable": True},
    "custom_model": {"is_custom_model": True},
    "conversation": {},
    "message": {},
    "knowledge_item": {},
    "sensor": {},
    "task": {},
}

def get_property(element, key, default=None):
    """获取属性：优先 extra，其次 category 默认值"""
    if key in element.extra:
        return element.extra[key]
    return CATEGORY_DEFAULTS.get(element.category, {}).get(key, default)
```

**便捷方法**：

```python
element.is_space()        # 是否为空间类型
element.is_toggleable()   # 是否可切换状态
element.is_movable()      # 是否可自主移动
element.is_custom_model() # 是否为自定义模型
```

### 3.9 属性定义系统

**核心原则**：元素的编辑和展示应基于属性定义系统，避免硬编码。

| 规范 | 说明 |
|------|------|
| 类型来源 | 从 `element.category` 自动获取，不作为参数传入 |
| 属性定义 | 在 `ELEMENT_PROPERTY_DEFINITIONS` 中配置 |
| 扩展新类型 | 只需添加属性定义配置，无需修改 UI 代码 |

**属性定义结构**：

```python
@dataclass
class PropertyDefinition:
    key: str                    # 属性键
    display_name: str           # 显示名称
    property_type: PropertyType # 类型（TEXT, NUMBER, SELECT, COORDINATES 等）
    editable: bool = True       # 是否可编辑
    visible: bool = True        # 是否显示
    required: bool = False      # 是否必填
    default: Any = None         # 默认值
    unit: str = ""              # 单位
    # ... 其他配置

ELEMENT_PROPERTY_DEFINITIONS = {
    "device": {
        "base_properties": [...],      # 基础属性（name, type 等）
        "extra_properties": [...],     # 扩展属性（brand, model 等）
        "position_properties": [...],  # 位置属性（position, size 等）
        "display_order": ["name", "type", ...],  # 显示顺序
    },
    "furniture": {...},
    "item": {...},
    "room": {...},
}
```

**使用方式**：

```python
# 编辑对话框 - 自动从 element.category 获取类型
dialog = ElementEditDialog(parent, element, viewmodel)

# 详情展示 - 自动从 element.category 获取类型
display = ElementDetailDisplay(element, viewmodel)
text = display.get_display_text()
```

### 3.11 扩展示例

```python
# 普通 ball：使用默认配置
ball = SceneElement(id="ball_001", category="ball", extra={"can_pick_up": True})

# 特殊 ball：通过 extra 覆盖
earth = SceneElement(id="earth_001", category="ball", extra={"can_pick_up": False})
```

### 3.12 业务分类
业务类型通过 `category` 字段实现，用户可自定义：

| category | 说明 | 默认属性 |
|----------|------|----------|
| `room` | 房间 | is_space=True |
| `device` | 设备 | is_toggleable=True |
| `furniture` | 家具 | - |
| `item` | 物品 | - |
| `door` | 门 | - |
| `window` | 窗户 | - |
| `robot` | 机器人 | is_movable=True |
| `custom_model` | 自定义模型 | is_custom_model=True |
| `conversation` | 对话 | - |
| `message` | 消息 | - |
| `knowledge_item` | 知识条目 | - |
| `sensor` | 传感器 | - |
| `task` | 任务 | - |
| `...` | 用户自定义 | 自定义 |

---

## 4. 分层架构设计 (Layered Architecture)

### 4.1 核心理念

**数据与渲染彻底分离**：业务模型完全独立于渲染引擎，可随时切换渲染实现而不影响业务逻辑。

```
┌─────────────────────────────────────────────────────────────┐
│                    分层架构设计                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌─────────────────────────────────────────────────────┐  │
│    │              Model 层（业务世界）                    │  │
│    │                                                     │  │
│    │  职责：定义数据结构，不涉及渲染实现                 │  │
│    │  • 位置、尺寸、角度、类型、状态                     │  │
│    │  • 几何：球体/立方体/圆柱/STL/复杂模型              │  │
│    │  • 可完全不依赖任何渲染库                           │  │
│    │                                                     │  │
│    │  调试时：使用简单几何体代替                         │  │
│    │  展示时：切换为精细模型                             │  │
│    └─────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│    ┌─────────────────────────────────────────────────────┐  │
│    │              ActorFactory 层（转换器）               │  │
│    │                                                     │  │
│    │  职责：将业务模型转换为可渲染对象                   │  │
│    │  • 输入：任意 Model                                 │  │
│    │  • 输出：vtkActor（或其他引擎的绘制对象）           │  │
│    │                                                     │  │
│    │  职责范围：                                         │  │
│    │  • 绑定几何数据                                     │  │
│    │  • 设置颜色、透明度、样式                           │  │
│    │  • 不创建几何体、不编写业务逻辑                     │  │
│    └─────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│    ┌─────────────────────────────────────────────────────┐  │
│    │              View/Render 层（画布）                  │  │
│    │                                                     │  │
│    │  职责：负责渲染输出                                 │  │
│    │  • 窗口、相机、光照、交互                           │  │
│    │  • 添加/移除 Actor                                  │  │
│    │  • 拾取、旋转、缩放                                 │  │
│    │  • 不感知 Model 内部结构                            │  │
│    └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 一句话口诀

> **Model 定长相，Factory 转演员，Render 只管上场。**

### 4.3 核心价值

| 价值 | 说明 |
| --- | --- |
| **引擎无关** | 业务逻辑可脱离渲染引擎独立运行、测试 |
| **灵活切换** | 调试时使用简单几何体，展示时切换为精细模型 |
| **单一职责** | 每层只做一件事，边界清晰 |
| **可测试性** | Model 层可纯单元测试，无需渲染环境 |

### 4.4 层级职责对照

| 层级 | 输入 | 输出 | 职责边界 |
| --- | --- | --- | --- |
| **Model 层** | 业务数据 | SceneElement | 只定义数据结构，不依赖渲染库 |
| **ActorFactory 层** | SceneElement | vtkActor/引擎对象 | 只做渲染对象创建，不编写业务逻辑 |
| **View/Render 层** | Actor | 画面 | 只做渲染和交互，不感知 Model 结构 |

### 4.5 实现示例

```python
# ===== Model 层：纯业务数据，无渲染依赖 =====
@dataclass
class DeviceModel:
    """设备模型 - 完全不依赖 VTK"""
    id: str
    name: str
    position: List[float, float, float]
    geometry_type: str = "cube"  # cube, sphere, cylinder, custom
    size: List[float, float, float] = [0.5, 0.5, 0.5]
    
    def get_bounds(self) -> Bounds:
        """计算边界 - 纯数学运算"""
        x, y, z = self.position
        w, d, h = self.size
        return Bounds(
            min_x=x - w/2, max_x=x + w/2,
            min_y=y - d/2, max_y=y + d/2,
            min_z=z, max_z=z + h
        )


# ===== ActorFactory 层：Model → Actor 转换 =====
class DeviceActorFactory:
    """设备 Actor 工厂 - 只做渲染对象创建"""
    
    def create(self, model: DeviceModel) -> vtkActor:
        """根据 Model 创建 Actor"""
        # 选择几何源
        if model.geometry_type == "cube":
            source = vtk.vtkCubeSource()
        elif model.geometry_type == "sphere":
            source = vtk.vtkSphereSource()
        else:
            source = vtk.vtkCubeSource()
        
        # 设置几何参数
        source.SetCenter(*CoordTransform.lsh_to_vtk_position(model.position))
        source.SetXLength(model.size[0])
        source.SetYLength(model.size[2])
        source.SetZLength(model.size[1])
        
        # 创建 Actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetUserData(model.id)  # 关联 Model ID
        
        return actor
    
    def update(self, actor: vtkActor, model: DeviceModel):
        """更新 Actor 属性"""
        actor.SetPosition(*CoordTransform.lsh_to_vtk_position(model.position))
        # ... 其他属性更新


# ===== View/Render 层：只管渲染 =====
class VTK3DView:
    """VTK 3D 视图 - 只负责渲染和交互"""
    
    def __init__(self):
        self._renderer = vtk.vtkRenderer()
        self._actors: Dict[str, vtkActor] = {}
    
    def add_actor(self, actor_id: str, actor: vtkActor):
        """添加 Actor - 不感知 Model 结构"""
        self._actors[actor_id] = actor
        self._renderer.AddActor(actor)
    
    def remove_actor(self, actor_id: str):
        """移除 Actor"""
        if actor_id in self._actors:
            self._renderer.RemoveActor(self._actors[actor_id])
            del self._actors[actor_id]
    
    def render(self):
        """渲染画面"""
        self._render_window.Render()
```

### 4.6 设计原则

| 原则 | 说明 |
| --- | --- |
| **Model 纯净** | Model 类不导入任何渲染库（vtk, godot, three.js 等） |
| **Factory 单向** | Factory 只从 Model 读取数据，不修改 Model |
| **View 无知** | View 不知道 Model 的存在，只操作 Actor |
| **依赖方向** | View → Actor → Model，单向依赖 |

### 4.7 禁止行为

| 禁止 | 原因 |
| --- | --- |
| ❌ Model 层导入渲染库 | 破坏引擎无关性 |
| ❌ Factory 写业务逻辑 | 违反单一职责 |
| ❌ View 直接操作 Model | 跨层调用，耦合严重 |
| ❌ Actor 存储业务状态 | Actor 只是渲染壳，状态应在 Model |

### 4.8 核心洞察

> 即使移除 VTK 渲染引擎，业务模型逻辑仍保持完整，仅需替换渲染实现即可恢复可视化功能。

这意味着：
- 业务逻辑可独立测试、独立演进
- 渲染引擎可随时替换（VTK → Godot → Three.js）
- 调试时使用简单几何体，发布时切换为精细模型

---

## 5. 动机 (Motivation)

### 5.1 问题背景

在虚拟世界可视化系统中，同一数据需要在多个视图中展示：

| 视图类型 | 展示形式 | 数据维度  |
| -------- | -------- | --------- |
| 结构视图 | 树形列表 | 层级关系  |
| 2D 视图  | 平面图标 | (x, y)    |
| 3D 视图  | 立体模型 | (x, y, z) |
| 列表视图 | 表格行   | 状态信息  |

传统做法是在数据变化时手动调用各视图的更新方法，存在以下问题：

1. **耦合度高**：数据层需要知道所有视图的存在
2. **易遗漏**：新增视图时容易忘记添加更新调用
3. **不一致**：不同操作的更新逻辑分散，难以维护

### 5.2 解决方案

LSH 协议采用**发布-订阅模式**，将数据变化抽象为事件：

```
数据变化 → 发布事件 → 所有订阅者自动响应
```

视图只需订阅自己关心的事件，无需知道数据来源，实现完全解耦。

---

## 6. 术语定义 (Terminology)

| 术语                              | 定义                                                  |
| --------------------------------- | ----------------------------------------------------- |
| **事件 (Event)**            | 数据变化的抽象表示，包含事件类型、目标 ID、位置信息等 |
| **发布者 (Publisher)**      | 产生事件的组件，通常是数据操作层                      |
| **订阅者 (Subscriber)**     | 接收并响应事件的组件，通常是视图层                    |
| **位置数据 (PositionData)** | 三维空间坐标，包含 x、y、z 分量                       |
| **尺寸数据 (SizeData)**     | 三维尺寸，包含 width、depth、height 分量              |
| **批量模式 (Batch Mode)**   | 事件合并模式，多个事件合并为一次更新                  |
| **空间 (Space)**            | 有边界的容器，可包含其他空间和实体                    |
| **实体 (Entity)**           | 场景中的可交互对象                                    |

---

## 7. 坐标系统 (Coordinate System)

### 7.1 统一坐标系

LSH 协议采用**右手坐标系**（建筑/BIM 风格），所有视图必须遵循统一的坐标系统：

```
Z ↑ (高度/height)
  │
  │     ┌─────────┐
  │     │  空间   │
  │     │  Space  │
  │     └─────────┘
  │
  └──────────────────────→ X (宽度/width)
Y (深度/depth，向前)
```

| 轴             | 方向     | 说明     | 对应尺寸      |
| -------------- | -------- | -------- | ------------- |
| **X 轴** | 向右为正 | 水平方向 | width (宽度)  |
| **Y 轴** | 向前为正 | 深度方向 | depth (深度)  |
| **Z 轴** | 向上为正 | 高度方向 | height (高度) |

**坐标系选择原因**：

1. **建筑/BIM 习惯**：地面是 X-Y 平面，平面图直接对应
2. **直觉性**：Z 轴向上，符合"高度"概念
3. **俯视图兼容**：俯视图直接是 X-Y 平面，无需坐标转换

### 7.2 视图坐标适配

| 视图                      | 原始坐标系 | 适配方式                                        |
| ------------------------- | ---------- | ----------------------------------------------- |
| **2D 视图 (Qt)** | Y 轴向下 | `scale(1, -1)` 翻转 Y 轴，俯视图显示 X-Y 平面 |
| **3D 视图 (VTK)** | Y 轴向上 | 转换公式：VTK(X, Y, Z) = LSH(X, Z, Y) |
| **3D 视图 (Godot)** | Z 轴向后 | 转换公式：Godot(X, Y, Z) = LSH(X, Z, -Y) |
| **结构视图**        | 无坐标     | 不涉及                                          |

### 7.3 3D 引擎坐标转换规范

不同 3D 引擎使用不同的坐标系，LSH 协议定义统一的转换规范：

#### 7.3.1 坐标系对比

| 引擎               | X 轴         | Y 轴         | Z 轴          | 坐标系类型 |
| ------------------ | ------------ | ------------ | ------------- | ---------- |
| **LSH 协议** | 向右 (width) | 向前 (depth) | 向上 (height) | 右手坐标系 |
| **VTK**      | 向右         | 向上         | 向前          | 右手坐标系 |
| **Godot**    | 向右         | 向上         | 向后          | 左手坐标系 |
| **Blender**  | 向右         | 向前         | 向上          | 右手坐标系 |
| **Three.js** | 向右         | 向上         | 向前          | 右手坐标系 |

**说明**：LSH 协议与 Blender 坐标系完全一致（建筑/BIM 风格）。

#### 7.3.2 转换公式

**LSH → Godot**：

```
Godot(X, Y, Z) = LSH(X, Z, -Y)

其中：
- Godot.X = LSH.X（宽度不变）
- Godot.Y = LSH.Z（高度映射）
- Godot.Z = -LSH.Y（深度取负，因为 Godot Z 轴向后）
```

**Godot → LSH**：

```
LSH(X, Y, Z) = Godot(X, -Z, Y)

其中：
- LSH.X = Godot.X
- LSH.Y = -Godot.Z
- LSH.Z = Godot.Y
```

**LSH → VTK**：

```
VTK(X, Y, Z) = LSH(X, Z, Y)

其中：
- VTK.X = LSH.X（宽度不变）
- VTK.Y = LSH.Z（高度映射）
- VTK.Z = LSH.Y（深度映射）
```

**LSH → Blender**：

```
无需转换，坐标系完全一致
Blender(X, Y, Z) = LSH(X, Y, Z)
```

#### 7.3.3 尺寸转换

尺寸只做轴映射，不取负值：

| LSH        | Godot      | VTK        | Blender    |
| ---------- | ---------- | ---------- | ---------- |
| width (X)  | width (X)  | width (X)  | width (X)  |
| depth (Y)  | depth (Z)  | depth (Z)  | depth (Y)  |
| height (Z) | height (Y) | height (Y) | height (Z) |

**说明**：LSH 与 Blender 尺寸完全一致。

#### 7.3.4 边界转换

**LSH → Godot 边界**：

```python
def lsh_to_godot_bounds(lsh_min, lsh_max):
    return {
        "min": [lsh_min[0], lsh_min[2], -lsh_max[1]],
        "max": [lsh_max[0], lsh_max[2], -lsh_min[1]]
    }
```

**Godot → LSH 边界**：

```python
def godot_to_lsh_bounds(godot_min, godot_max):
    return {
        "min": [godot_min[0], -godot_max[2], godot_min[1]],
        "max": [godot_max[0], -godot_min[2], godot_max[1]]
    }
```

**LSH → VTK 边界**：

```python
def lsh_to_vtk_bounds(lsh_min, lsh_max):
    return {
        "min": [lsh_min[0], lsh_min[2], lsh_min[1]],
        "max": [lsh_max[0], lsh_max[2], lsh_max[1]]
    }
```

**LSH ↔ Blender**：无需转换

#### 7.3.5 实现规范

**统一转换层**：

所有 3D 引擎适配器必须在数据发送端统一转换，接收端直接使用：

```python
# Python 端统一转换模块
class CoordTransform:
    """坐标转换工具
  
    LSH 坐标系：X=右(width), Y=前(depth), Z=上(height)
    """
  
    @staticmethod
    def lsh_to_godot_position(pos: tuple) -> list:
        x, y, z = pos[0], pos[1], pos[2] if len(pos) > 2 else 0
        return [x, z, -y]  # X不变, Z→Y, Y→-Z
  
    @staticmethod
    def lsh_to_godot_size(size: tuple) -> list:
        w, d, h = size[0], size[1], size[2] if len(size) > 2 else 0
        return [w, h, d]  # width→X, height→Y, depth→Z
  
    @staticmethod
    def lsh_to_vtk_position(pos: tuple) -> list:
        x, y, z = pos[0], pos[1], pos[2] if len(pos) > 2 else 0
        return [x, z, y]  # X不变, Z→Y, Y→Z
  
    @staticmethod
    def lsh_to_vtk_size(size: tuple) -> list:
        w, d, h = size[0], size[1], size[2] if len(size) > 2 else 0
        return [w, h, d]  # width→X, height→Y, depth→Z
  
    @staticmethod
    def godot_to_lsh_bounds(min_pos: tuple, max_pos: tuple) -> tuple:
        lsh_min = [min_pos[0], -max_pos[2], min_pos[1]]
        lsh_max = [max_pos[0], -min_pos[2], max_pos[1]]
        return lsh_min, lsh_max
```

**引擎适配器职责**：

| 层级                | 职责     | 说明                          |
| ------------------- | -------- | ----------------------------- |
| **Python 端** | 数据转换 | 发送前转换为引擎坐标系        |
| **引擎端**    | 直接使用 | 接收数据直接渲染，不再转换    |
| **返回数据**  | 逆向转换 | 边界等返回数据转回 LSH 坐标系 |

#### 7.3.6 内外坐标系分离架构

**核心原则**：系统对外统一使用 LSH 坐标系，内部渲染层做透明转换。

```
┌─────────────────────────────────────────────────────────────┐
│                    内外坐标系分离架构                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌─────────────────────────────────────────────────────┐  │
│    │                 外部接口层 (LSH)                     │  │
│    │                                                     │  │
│    │  • 数据输入：position=(x, y, z) = (右, 前, 上)      │  │
│    │  • 数据输出：bounds, position 等                    │  │
│    │  • API 参数：全部使用 LSH 坐标系                    │  │
│    │  • 用户交互：鼠标拾取、位置选择等                   │  │
│    └─────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│    ┌─────────────────────────────────────────────────────┐  │
│    │              坐标转换层 (适配器)                     │  │
│    │                                                     │  │
│    │  • LSH → 引擎坐标：渲染前转换                       │  │
│    │  • 引擎 → LSH：返回数据转换                         │  │
│    │  • 对业务层透明                                     │  │
│    └─────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│    ┌─────────────────────────────────────────────────────┐  │
│    │              内部渲染层 (引擎坐标)                   │  │
│    │                                                     │  │
│    │  • VTK: X=右, Y=上, Z=前                            │  │
│    │  • Godot: X=右, Y=上, Z=后                          │  │
│    │  • 引擎内部操作使用引擎原生坐标系                   │  │
│    └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**架构规则**：

| 规则                     | 说明                                           |
| ------------------------ | ---------------------------------------------- |
| **输入数据使用 LSH** | 所有外部输入（API、文件、用户操作）使用 LSH 坐标系 |
| **输出数据使用 LSH** | 所有外部输出（查询结果、边界、位置）使用 LSH 坐标系 |
| **内部渲染层转换** | 只在渲染引擎适配层做坐标转换，业务层无感知     |
| **单一转换点**     | 每个引擎只有一个转换入口，避免分散             |

**实现示例**：

```python
class VTK3DView:
    """VTK 3D 视图 - 遵循内外坐标系分离架构"""
    
    # ===== 外部接口（LSH 坐标系）=====
    
    def add_room(self, room_id: str, position: tuple, size: tuple):
        """添加房间（外部接口，使用 LSH 坐标系）
        
        Args:
            position: (x, y, z) = (右, 前, 上)
            size: (width, depth, height)
        """
        # 内部转换并渲染
        vtk_pos = CoordTransform.lsh_to_vtk_position(position)
        vtk_size = CoordTransform.lsh_to_vtk_size(size)
        self._create_box(vtk_pos, vtk_size)
    
    def get_scene_bounds(self) -> tuple:
        """获取场景边界（外部接口，返回 LSH 坐标系）"""
        vtk_bounds = self._get_vtk_bounds()
        return CoordTransform.vtk_to_lsh_bounds(vtk_bounds)
    
    # ===== 内部渲染（VTK 坐标系）=====
    
    def _create_box(self, vtk_pos: tuple, vtk_size: tuple):
        """创建盒子（内部方法，使用 VTK 坐标系）"""
        # 直接使用 VTK 坐标系渲染
        box = vtk.vtkCubeSource()
        box.SetCenter(*vtk_pos)
        box.SetXLength(vtk_size[0])
        box.SetYLength(vtk_size[1])
        box.SetZLength(vtk_size[2])
```

**禁止行为**：

| 禁止                                     | 原因                         |
| ---------------------------------------- | ---------------------------- |
| ❌ 业务层直接使用引擎坐标系             | 破坏架构一致性               |
| ❌ 在多处分散做坐标转换                 | 难以维护，容易出错           |
| ❌ 外部接口暴露引擎坐标                 | 增加调用方负担               |
| ❌ 返回数据未转换回 LSH                 | 违反输入输出一致性原则       |

### 7.4 文字标签处理

由于 2D 视图翻转了 Y 轴，文字标签需要额外处理：

```python
# 文字标签翻转恢复正常显示
label.setTransform(QTransform().scale(1, -1))

# 位置计算示例
# 空间名称：居中显示在空间上方
label.setPos((w - label_width) / 2, (h + label_height) / 2)

# 空间尺寸：显示在空间下方
info_label.setPos((w - info_width) / 2, 5 + info_height)
```

### 7.5 2D 视图坐标转换

2D 视图显示俯视图（X-Y 平面），需要将 3D 坐标投影到 2D：

```python
# 3D 坐标 → 2D 俯视图坐标
def to_2d_top_view(pos: PositionData) -> tuple:
    """将 3D 坐标转换为 2D 俯视图坐标
  
    俯视图显示 X-Y 平面（地面），Z 轴（高度）被忽略
    """
    return (pos.x, pos.y)  # X=水平，Y=垂直（深度）

# 2D 俯视图坐标 → 3D 坐标
def from_2d_top_view(x: float, y: float, z: float = 0.0) -> PositionData:
    """将 2D 俯视图坐标转换为 3D 坐标
  
    Args:
        x: 2D 水平坐标（对应 3D X 轴，宽度）
        y: 2D 垂直坐标（对应 3D Y 轴，深度）
        z: 3D 高度（默认 0）
    """
    return PositionData(x=x, y=y, z=z)
```

---

## 8. 数据结构 (Data Structures)

### 8.1 位置数据 (PositionData)

```python
@dataclass
class PositionData:
    """三维空间位置"""
    x: float = 0.0  # X 轴坐标（米）
    y: float = 0.0  # Y 轴坐标（米）
    z: float = 0.0  # Z 轴坐标（米）
  
    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}
  
    @classmethod
    def from_dict(cls, data: Dict) -> 'PositionData':
        return cls(
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
            z=data.get("z", 0.0)
        )
```

### 8.2 尺寸数据 (SizeData)

```python
@dataclass
class SizeData:
    """三维尺寸
  
    与坐标系对应：
    - width: X 轴方向尺寸（宽度）
    - depth: Y 轴方向尺寸（深度）
    - height: Z 轴方向尺寸（高度）
    """
    width: float = 1.0   # 宽度（米），X 轴方向
    depth: float = 1.0   # 深度（米），Y 轴方向
    height: float = 1.0  # 高度（米），Z 轴方向
  
    def to_dict(self) -> Dict[str, float]:
        return {"width": self.width, "depth": self.depth, "height": self.height}
```

### 8.3 边界数据 (Bounds)

```python
@dataclass
class Bounds:
    """空间边界
  
    定义空间的范围，用于：
    1. 渲染优化（视锥剔除）
    2. 碰撞检测
    3. 导航网格生成
    """
    min_x: float = 0.0
    max_x: float = 1.0
    min_y: float = 0.0
    max_y: float = 1.0
    min_z: float = 0.0
    max_z: float = 1.0
  
    @property
    def width(self) -> float:
        return self.max_x - self.min_x
  
    @property
    def depth(self) -> float:
        return self.max_y - self.min_y
  
    @property
    def height(self) -> float:
        return self.max_z - self.min_z
  
    @property
    def center(self) -> List[float, float, float]:
        return (
            (self.min_x + self.max_x) / 2,
            (self.min_y + self.max_y) / 2,
            (self.min_z + self.max_z) / 2
        )
  
    def contains_point(self, x: float, y: float, z: float) -> bool:
        """检查点是否在边界内"""
        return (
            self.min_x <= x <= self.max_x and
            self.min_y <= y <= self.max_y and
            self.min_z <= z <= self.max_z
        )
```

### 8.4 事件数据 (ViewSyncEvent)

```python
@dataclass
class ViewSyncEvent:
    """视图同步事件"""
    event_type: ViewSyncEvents           # 事件类型
    target_id: str                       # 目标对象 ID
    target_type: str = ""                # 目标类型（space/entity）
    position: Optional[PositionData] = None  # 位置信息
    size: Optional[SizeData] = None          # 尺寸信息
    parent_id: Optional[str] = None          # 父元素 ID（层级变化时）
    extra: Dict[str, Any] = field(default_factory=dict)  # 扩展字段
```

### 8.5 场景元素 (SceneElement)

```python
@dataclass
class SceneElement:
    """统一元素模型 - 万物皆元素
    
    所有元素（虚拟/现实）都使用此模型，便于：
    1. 统一搜索
    2. 跨视图高亮
    3. LSH 同步
    
    v3.0: 移除 element_type，统一通过 category 区分
    """
    id: str                              # 元素唯一标识
    name: str                            # 元素名称
    category: str = ""                   # 业务分类（room, device, furniture 等）
  
    # 变换属性
    position: List[float, float, float] = [0.0, 0.0, 0.0]
    rotation: List[float, float, float] = [0.0, 0.0, 0.0]
    scale: float = 1.0
  
    # 尺寸信息
    size: List[float, float, float] = [1.0, 1.0, 1.0]
  
    # 边界（空间类型需要）
    bounds: Optional[Bounds] = None
  
    # 层级关系
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    hierarchy_policy: HierarchyPolicy = HierarchyPolicy.FOLLOW_PARENT
    local_position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    local_rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
  
    # 模板引用
    template_id: Optional[str] = None
  
    # 标签
    tags: List[str] = field(default_factory=list)
  
    # 扩展数据
    extra: Dict[str, Any] = field(default_factory=dict)
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
  
    # 可见性
    visible: bool = True
    searchable: bool = True
    
    # ===== 属性查询方法 =====
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """获取属性：优先 extra，其次 CATEGORY_DEFAULTS[category]"""
        pass
    
    def is_space(self) -> bool:
        """是否为空间类型（有空间边界）"""
        return self.get_property("is_space", False)
    
    def is_toggleable(self) -> bool:
        """是否可切换状态"""
        return self.get_property("is_toggleable", False)
    
    def is_movable(self) -> bool:
        """是否可自主移动"""
        return self.get_property("is_movable", False)
    
    def is_custom_model(self) -> bool:
        """是否为自定义导入模型"""
        return self.get_property("is_custom_model", False)
```

**extra 字段设计原则**：

`extra` 是一个灵活的扩展字段，用于存储与元素相关的额外数据。但有以下限制：

1. **只存储简单数据**：字符串、数字、布尔值、列表、字典
2. **不存储复杂对象**：不应存储 SceneElement 或其他复杂对象
3. **关联元素使用 ID 引用**：如需关联其他元素，使用 `parent_id`/`children_ids` 或存储 ID 列表

```python
# ✅ 正确用法
device.set_extra_property("room_id", "room_001")
device.set_extra_property("state", "on")
device.set_extra_property("power", 60)

# ❌ 错误用法
device.set_extra_property("room", room_object)  # 不应存储对象
```

**典型用途**：

| 元素类型 | extra 中存储的内容 |
|---------|-------------------|
| 房间 | `room_type`, `device_ids`, `component_ids` |
| 设备 | `device_type`, `state`, `room_id` |
| 家具 | `furniture_type`, `room_id` |
| 物品 | `item_type`, `quantity`, `expiry_date` |

### 8.6 元素注册表 (SceneElementRegistry)

```python
class SceneElementRegistry:
    """元素注册表
    
    统一管理所有元素，支持：
    1. 注册/注销元素
    2. 按分类/标签搜索
    3. 层级关系管理
    """
  
    def register(self, element: SceneElement) -> None:
        """注册元素"""
        pass
  
    def unregister(self, element_id: str) -> Optional[SceneElement]:
        """注销元素（级联删除子元素）"""
        pass
  
    def get(self, element_id: str) -> Optional[SceneElement]:
        """获取元素"""
        pass
  
    def get_all(self) -> List[SceneElement]:
        """获取所有元素"""
        pass
  
    def get_by_category(self, category: str) -> List[SceneElement]:
        """按分类获取元素"""
        pass
  
    def get_by_tag(self, tag: str) -> List[SceneElement]:
        """按标签获取元素"""
        pass
  
    def get_children(self, parent_id: str) -> List[SceneElement]:
        """获取子元素"""
        pass
  
    def get_parent(self, element_id: str) -> Optional[SceneElement]:
        """获取父元素"""
        pass
  
    def search(self, query: str, categories: List[str] = None, 
               tags: List[str] = None) -> List[SceneElement]:
        """搜索元素"""
        pass
  
    def update_position_cascade(self, element_id: str, 
                                 new_position: List[float, float, float]) -> None:
        """级联更新位置（父元素移动时自动更新子元素）"""
        pass
```

---

## 9. 事件类型 (Event Types)

### 9.1 统一元素事件

LSH 协议 v2.0.0 统一使用 `ELEMENT_*` 事件，通过 `target_type` 区分 SPACE/ENTITY，通过 `extra.category` 区分业务类型：

| 事件类型                       | 值                             | 携带数据              | 说明             |
| ------------------------------ | ------------------------------ | --------------------- | ---------------- |
| `ELEMENT_ADDED`              | `element_added`              | position, size, extra | 元素添加         |
| `ELEMENT_DELETED`            | `element_deleted`            | extra                 | 元素删除         |
| `ELEMENT_CHANGED`            | `element_changed`            | position, size, extra | 元素属性变化     |
| `ELEMENT_POSITION_CHANGED`   | `element_position_changed`   | position              | 元素位置变化     |
| `ELEMENT_VISIBILITY_CHANGED` | `element_visibility_changed` | extra.visible         | 元素可见性变化   |
| `ELEMENT_HIERARCHY_CHANGED`  | `element_hierarchy_changed`  | parent_id, extra      | 元素层级关系变化 |
| `ELEMENTS_SYNC`              | `elements_sync`              | extra.elements        | 批量同步所有元素 |

### 9.2 场景事件

| 事件类型                 | 值                       | 携带数据                                         | 说明         |
| ------------------------ | ------------------------ | ------------------------------------------------ | ------------ |
| `SCENE_ACTIVATED`      | `scene_activated`      | extra.scene_id                                   | 场景激活     |
| `SCENE_CHANGED`        | `scene_changed`        | extra                                            | 场景变化     |
| `SCENE_BOUNDS_CHANGED` | `scene_bounds_changed` | extra.{min_x, max_x, min_y, max_y, min_z, max_z} | 场景边界变化 |

### 9.3 编辑模式事件

| 事件类型              | 值                    | 携带数据      | 说明         |
| --------------------- | --------------------- | ------------- | ------------ |
| `EDIT_MODE_CHANGED` | `edit_mode_changed` | extra.enabled | 编辑模式切换 |

### 9.4 路径规划事件

#### 9.4.1 基础路径事件

| 事件类型                   | 值                         | 携带数据                                          | 说明         |
| -------------------------- | -------------------------- | ------------------------------------------------- | ------------ |
| `PATH_CALCULATED`        | `path_calculated`        | extra.{path, distance, estimated_time, waypoints} | 路径计算完成 |
| `PATH_VISUALIZED`        | `path_visualized`        | extra.{path, view_type, color, clear_previous}    | 路径可视化   |
| `PATH_EXECUTED`          | `path_executed`          | extra.{success, message}                          | 路径执行完成 |
| `NAVIGATION_MAP_UPDATED` | `navigation_map_updated` | extra.{grid_info}                                 | 导航地图更新 |

#### 9.4.2 路径选择事件

| 事件类型                        | 值                              | 携带数据                           | 说明             |
| ------------------------------- | ------------------------------- | ---------------------------------- | ---------------- |
| `PATH_START_SELECTED`         | `path_start_selected`         | position, target_id (element_id)   | 路径起点选择     |
| `PATH_END_SELECTED`           | `path_end_selected`           | position, target_id (element_id)   | 路径终点选择     |
| `PATH_WAYPOINT_ADDED`         | `path_waypoint_added`         | position, target_id, extra.{index} | 添加途径点       |
| `PATH_WAYPOINT_REMOVED`       | `path_waypoint_removed`       | position, target_id, extra.{index} | 移除途径点       |
| `PATH_WAYPOINTS_CLEARED`      | `path_waypoints_cleared`      | -                                  | 清除所有途径点   |
| `PATH_SELECTION_MODE_CHANGED` | `path_selection_mode_changed` | extra.mode                         | 路径选择模式变化 |
| `PATH_SELECTION_CLEARED`      | `path_selection_cleared`      | -                                  | 路径选择清除     |

#### 9.4.3 路径规划模式事件

| 事件类型                            | 值                                  | 携带数据                                   | 说明             |
| ----------------------------------- | ----------------------------------- | ------------------------------------------ | ---------------- |
| `PATH_PLANNING_MODE_CHANGED`      | `path_planning_mode_changed`      | extra.{mode, config}                       | 路径规划模式变化 |
| `PATH_OBSTACLE_AVOIDANCE_CHANGED` | `path_obstacle_avoidance_changed` | extra.{enabled, obstacles}                 | 避障设置变化     |
| `PATH_COVERAGE_MODE_CHANGED`      | `path_coverage_mode_changed`      | extra.{enabled, algorithm, area_bounds}    | 覆盖模式设置变化 |
| `PATH_COVERAGE_PROGRESS`          | `path_coverage_progress`          | extra.{progress, covered_area, total_area} | 覆盖进度更新     |
| `PATH_COVERAGE_COMPLETED`         | `path_coverage_completed`         | extra.{success, coverage_rate, path}       | 覆盖完成         |

### 9.5 路径规划数据结构

#### 9.5.1 路径规划配置

```python
@dataclass
class PathPlanningConfig:
    """路径规划配置"""
  
    # 基础配置
    algorithm: str = "a_star"          # 算法类型: a_star, dijkstra, rrt, rrt_star, bfs, potential_field
    resolution: float = 0.1            # 网格分辨率（米）
  
    # 避障配置
    obstacle_avoidance: bool = True    # 是否启用避障
    obstacle_margin: float = 0.2       # 障碍物边距（米）
    dynamic_obstacles: List[str] = field(default_factory=list)  # 动态障碍物ID列表
  
    # 途径点配置
    waypoints: List[PositionData] = field(default_factory=list)  # 途径点列表
    waypoint_order: str = "optimal"    # 途径点顺序: optimal（最优）, fixed（固定）
  
    # 覆盖模式配置
    coverage_mode: bool = False        # 是否启用覆盖模式
    coverage_algorithm: str = "sweep"  # 覆盖算法: sweep, zigzag, spiral
    coverage_width: float = 0.3        # 覆盖宽度（米），适用于扫地机器人
    coverage_overlap: float = 0.1      # 覆盖重叠率（百分比）
  
    # 路径优化
    smooth_path: bool = True           # 是否平滑路径
    simplify_path: bool = True         # 是否简化路径
```

#### 9.5.2 路径规划模式

```python
class PathPlanningMode(Enum):
    """路径规划模式"""
    NORMAL = "normal"                  # 普通模式：起点→终点
    WITH_WAYPOINTS = "waypoints"       # 途径点模式：起点→途径点→终点
    COVERAGE = "coverage"              # 覆盖模式：全覆盖路径（扫地机器人）
    OBSTACLE_AVOIDANCE = "avoidance"   # 避障模式：动态避障
```

#### 9.5.3 覆盖路径结果

```python
@dataclass
class CoveragePathResult:
    """覆盖路径结果"""
    path: List[PositionData]           # 完整覆盖路径
    total_distance: float              # 总距离（米）
    estimated_time: float              # 预估时间（秒）
    coverage_area: float               # 覆盖面积（平方米）
    coverage_rate: float               # 覆盖率（百分比）
    missed_areas: List[Bounds]         # 未覆盖区域
    algorithm: str                     # 使用的算法
```

### 9.6 路径规划交互流程

#### 9.6.1 普通路径规划流程

```
1. 点击"路径规划"按钮 → 进入路径选择模式
2. 选择起点元素 → 发布 PATH_START_SELECTED 事件
3. 选择终点元素 → 发布 PATH_END_SELECTED 事件
4. （可选）配置避障 → 发布 PATH_OBSTACLE_AVOIDANCE_CHANGED 事件
5. 执行路径规划 → 发布 PATH_CALCULATED 事件
6. 可视化路径 → 发布 PATH_VISUALIZED 事件
```

#### 9.6.2 途径点路径规划流程

```
1. 点击"路径规划"按钮 → 进入路径选择模式
2. 选择起点元素 → 发布 PATH_START_SELECTED 事件
3. 添加途径点 → 发布 PATH_WAYPOINT_ADDED 事件（可多次）
4. 选择终点元素 → 发布 PATH_END_SELECTED 事件
5. 执行路径规划 → 发布 PATH_CALCULATED 事件
```

#### 8.6.3 覆盖模式流程（扫地机器人）

```
1. 点击"路径规划"按钮 → 进入路径选择模式
2. 启用覆盖模式 → 发布 PATH_COVERAGE_MODE_CHANGED 事件
3. 选择覆盖区域（房间或自定义区域）
4. 配置覆盖参数（宽度、重叠率等）
5. 执行覆盖规划 → 发布 PATH_CALCULATED 事件
6. 执行覆盖任务 → 发布 PATH_COVERAGE_PROGRESS 事件（进度更新）
7. 覆盖完成 → 发布 PATH_COVERAGE_COMPLETED 事件
```

### 8.7 模型模板事件

| 事件类型                   | 值                         | 携带数据              | 说明         |
| -------------------------- | -------------------------- | --------------------- | ------------ |
| `MODEL_TEMPLATE_ADDED`   | `model_template_added`   | extra.{template_data} | 模型模板添加 |
| `MODEL_TEMPLATE_UPDATED` | `model_template_updated` | extra.{template_data} | 模型模板更新 |
| `MODEL_TEMPLATE_REMOVED` | `model_template_removed` | target_id             | 模型模板移除 |

### 8.8 全局事件

| 事件类型            | 值                  | 携带数据                                | 说明                 |
| ------------------- | ------------------- | --------------------------------------- | -------------------- |
| `LAYOUT_LOADED`   | `layout_loaded`   | -                                       | 布局加载完成         |
| `LAYOUT_CHANGED`  | `layout_changed`  | -                                       | 布局变化             |
| `LAYOUT_CENTERED` | `layout_centered` | position (offset_x, offset_y, offset_z) | 布局居中（整体移动） |
| `FULL_REFRESH`    | `full_refresh`    | -                                       | 全量刷新             |

---

## 9. 协议接口 (API Specification)

### 9.1 管理器接口

```python
class ViewSyncManager:
    """视图同步管理器（单例）"""
  
    @classmethod
    def instance(cls) -> 'ViewSyncManager':
        """获取单例实例"""
        pass
  
    def subscribe(self, event_type: ViewSyncEvents, 
                  callback: Callable[[ViewSyncEvent], None]) -> None:
        """订阅事件
      
        Args:
            event_type: 事件类型
            callback: 回调函数，接收 ViewSyncEvent 参数
        """
        pass
  
    def unsubscribe(self, event_type: ViewSyncEvents, 
                    callback: Callable) -> None:
        """取消订阅"""
        pass
  
    def publish(self, event: ViewSyncEvent) -> None:
        """发布事件"""
        pass
  
    def batch_begin(self) -> None:
        """开始批量模式"""
        pass
  
    def batch_end(self) -> None:
        """结束批量模式，统一处理缓存的事件"""
        pass
  
    def enable(self) -> None:
        """启用同步"""
        pass
  
    def disable(self) -> None:
        """禁用同步"""
        pass
```

### 9.2 元素事件发布方法

```python
# === 元素事件 ===

def publish_element_added(self, element: SceneElement) -> None:
    """发布元素添加事件
    
    Args:
        element: 元素对象
    """
    pass

def publish_element_deleted(self, element_id: str, category: str = "", 
                            extra: dict = None) -> None:
    """发布元素删除事件"""
    pass

def publish_element_changed(self, element: SceneElement, changes: dict = None) -> None:
    """发布元素变化事件"""
    pass

def publish_element_position_changed(self, element_id: str, category: str,
                                     x: float, y: float, z: float = 0.0,
                                     source: str = None) -> None:
    """发布元素位置变化事件"""
    pass

def publish_element_visibility_changed(self, element_id: str, category: str,
                                       visible: bool) -> None:
    """发布元素可见性变化事件"""
    pass

def publish_element_hierarchy_changed(self, element_id: str, category: str,
                                      old_parent_id: str = None, 
                                      new_parent_id: str = None) -> None:
    """发布元素层级关系变化事件"""
    pass

def publish_elements_sync(self, elements: List[SceneElement]) -> None:
    """发布元素批量同步事件"""
    pass

# === 全局事件 ===

def publish_full_refresh(self) -> None:
    """发布全量刷新事件"""
    pass

def publish_layout_loaded(self) -> None:
    """发布布局加载完成事件"""
    pass

def publish_layout_changed(self) -> None:
    """发布布局变化事件"""
    pass

def publish_layout_centered(self, offset_x: float, offset_y: float, 
                            offset_z: float) -> None:
    """发布布局居中事件"""
    pass

def publish_scene_bounds_changed(self, min_x: float, max_x: float, 
                                  min_y: float, max_y: float,
                                  min_z: float, max_z: float) -> None:
    """发布场景边界变化事件"""
    pass

def publish_edit_mode_changed(self, enabled: bool) -> None:
    """发布编辑模式变化事件"""
    pass

# === 路径规划事件 ===

def publish_path_calculated(self, path: List, distance: float, 
                            estimated_time: float, waypoints: List = None) -> None:
    """发布路径计算完成事件"""
    pass

def publish_path_visualized(self, path: List, view_type: str = "both",
                            color: str = "green", clear_previous: bool = True) -> None:
    """发布路径可视化事件"""
    pass

def publish_path_executed(self, path_id: str, success: bool, 
                          message: str = "") -> None:
    """发布路径执行事件"""
    pass

# === 模型模板事件 ===

def publish_model_template_added(self, template_id: str, template_data: Dict) -> None:
    """发布模型模板添加事件"""
    pass

def publish_model_template_updated(self, template_id: str, template_data: Dict) -> None:
    """发布模型模板更新事件"""
    pass

def publish_model_template_removed(self, template_id: str) -> None:
    """发布模型模板移除事件"""
    pass
```

---

## 10. 使用示例 (Examples)

### 10.1 创建元素

```python
from lsh import SceneElement, view_sync, ViewSyncEvents

# 创建房间元素
# position=(x, y, z) = (宽度方向, 深度方向, 高度方向)
# size=(width, depth, height) = (宽度, 深度, 高度)
room = SceneElement.create(
    id="room_001", 
    name="客厅", 
    category="room",
    position=(0, 0, 0),          # 原点位置
    size=(5.0, 4.0, 2.8),        # 宽5米, 深4米, 高2.8米
)

# 创建设备元素
# 灯的位置：房间中心偏移 (2.5, 2.0, 1.5)
# x=2.5 (宽度方向中心), y=2.0 (深度方向中心), z=1.5 (高度方向，离地1.5米)
device = SceneElement.create(
    id="device_001",
    name="智能灯",
    category="device",
    position=(2.5, 2.0, 1.5),    # 宽度中心, 深度中心, 离地1.5米
    parent_id="room_001",
    extra={"state": "off", "device_type": "light"}
)

# 发布元素添加事件
view_sync.publish_element_added(room)
view_sync.publish_element_added(device)
```

### 10.2 视图订阅事件

```python
class VTK3DView:
    def __init__(self):
        # 订阅元素事件
        view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, 
                           self._on_element_added)
        view_sync.subscribe(ViewSyncEvents.ELEMENT_POSITION_CHANGED, 
                           self._on_position_changed)
        view_sync.subscribe(ViewSyncEvents.ELEMENT_DELETED, 
                           self._on_element_deleted)
    
    def _on_element_added(self, event: ViewSyncEvent):
        """响应元素添加"""
        category = event.target_type  # 现在存储 category
        if category == "room":
            self._add_room(event.target_id, event.position, event.size)
        elif category == "device":
            self._add_device(event.target_id, event.position)
    
    def _on_position_changed(self, event: ViewSyncEvent):
        """响应位置变化"""
        category = event.target_type  # category 字符串
        self._update_position(event.target_id, event.position)
    
    def _on_element_deleted(self, event: ViewSyncEvent):
        """响应元素删除"""
        category = event.target_type
        if category == "custom_model":
            delete_file = event.extra.get("delete_file", False)
            self._remove_model(event.target_id, delete_file)
```

### 10.3 批量更新

```python
# 批量更新时合并事件，避免重复刷新
view_sync.batch_begin()
view_sync.publish_element_position_changed("room_001", "room", 2.0, 3.0, 0)
view_sync.publish_element_position_changed("room_001", "room", 2.5, 3.5, 0)  # 会被合并
view_sync.publish_element_position_changed("device_001", "device", 1.0, 1.0, 1.5)
view_sync.batch_end()  # 只触发两次刷新（room_001 和 device_001）
```

### 10.4 层级关系变化

```python
# 将设备从一个房间移动到另一个房间
view_sync.publish_element_hierarchy_changed(
    element_id="device_001",
    category="device",
    old_parent_id="room_001",
    new_parent_id="room_002"
)
```

### 10.5 元素搜索

```python
from lsh import SceneElementRegistry

registry = SceneElementRegistry()

# 注册元素
registry.register(room)
registry.register(device)

# 按分类搜索
rooms = registry.get_by_category("room")
devices = registry.get_by_category("device")

# 按标签搜索
tagged = registry.get_by_tag("smart")

# 关键词搜索
results = registry.search("灯", categories=["device"])

# 获取所有元素
all_elements = registry.get_all()

# 统计
print(f"总数: {registry.count()}")
print(f"按分类: {registry.count_by_category()}")
```

---

## 11. 扩展应用 (Extensions)

LSH 协议为以下功能提供基础：

### 11.1 路径规划

基于位置数据计算最优路径：

```python
def calculate_path(start_id: str, end_position: PositionData) -> List[PositionData]:
    """基于 LSH 位置数据计算路径"""
    start_element = registry.get(start_id)
    start_pos = PositionData(*start_element.position)
    # A* 或其他路径规划算法
    return pathfinding(start_pos, end_position)
```

### 11.2 仿真模拟

元素状态变化触发场景仿真：

```python
def on_element_changed(event: ViewSyncEvent):
    """元素变化触发仿真"""
    category = event.extra.get("category", "")
    if category == "device":
        state = event.extra.get("state")
        if state == "on":
            simulate_device_activation(event.target_id)
```

### 11.3 动画系统

位置变化驱动平滑动画：

```python
def on_position_changed(event: ViewSyncEvent):
    """位置变化驱动动画"""
    old_pos = get_current_position(event.target_id)
    new_pos = event.position
    animate_movement(event.target_id, old_pos, new_pos, duration=0.3)
```

### 11.4 多人协作

事件广播实现协同编辑：

```python
def broadcast_event(event: ViewSyncEvent):
    """广播事件到其他客户端"""
    websocket.send({
        "type": "lsh_event",
        "data": event.to_dict()
    })
```

---

## 12. 与其他协议对比 (Comparison)

| 协议          | 领域         | 位置支持 | 空间语义 | 批量优化 | 类型系统                        |
| ------------- | ------------ | -------- | -------- | -------- | ------------------------------- |
| **LSH** | 虚拟世界     | ✅ 原生  | ✅ 原生  | ✅       | 灵活（SPACE/ENTITY + category） |
| 观察者模式    | 通用         | ❌       | ❌       | ❌       | 无                              |
| Redux/Flux    | 前端状态管理 | ❌       | ❌       | ❌       | 无                              |
| MQTT          | 物联网通信   | ❌       | ❌       | ❌       | 无                              |
| OPC UA        | 工业自动化   | ❌       | ❌       | ❌       | 强类型                          |
| CRDT          | 分布式协作   | ❌       | ❌       | ✅       | 无                              |

---

## 13. 交互协议 (Interaction Protocol)

### 13.1 核心概念

**相机是观察者，不是操作对象**。用户操作的是场景中的模型（Actor/Element），相机只是提供观察视角。

```
┌─────────────────────────────────────────────────────────────┐
│                    交互概念模型                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    用户（操作者）                                            │
│         │                                                   │
│         ▼                                                   │
│    ┌─────────┐                                              │
│    │ 模型    │  ← 被操作的对象（Actor/Element）             │
│    │ Actor   │                                              │
│    └─────────┘                                              │
│         │                                                   │
│         ▼                                                   │
│    ┌─────────┐                                              │
│    │ 相机    │  ← 观察者（提供视角）                        │
│    │ Camera  │    不应被直接操作                            │
│    └─────────┘                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**术语对照**：

| 用户视角   | 实际操作 | 说明               |
| ---------- | -------- | ------------------ |
| "旋转视图" | 旋转模型 | 模型绕旋转中心旋转 |
| "平移视图" | 平移模型 | 模型在屏幕上移动   |
| "缩放视图" | 移动相机 | 相机靠近/远离模型  |

### 13.2 设计原则

LSH 交互协议定义了 3D 视图中的标准交互方式，遵循以下原则：

| 原则                     | 说明                                           |
| ------------------------ | ---------------------------------------------- |
| **模型为中心**     | 用户操作的是模型，相机只是观察者               |
| **相机与实体分离** | 相机操作和实体操作使用不同的鼠标按键，互不干扰 |
| **一致性**         | 所有实现必须遵循统一的交互规则                 |
| **直觉性**         | 交互方向与视觉反馈一致，符合用户直觉           |
| **可扩展**         | 支持自定义交互模式                             |

### 13.3 交互模式配置

**配置文件**：`config/interaction.json`

```json
{
    "interaction_modes": {
        "default": {
            "description": "VTK 默认交互",
            "rotate_view": "left_drag",
            "pan_view": "middle_drag",
            "zoom_view": "scroll"
        },
        "solidworks": {
            "description": "SolidWorks 风格交互",
            "rotate_view": "middle_drag",
            "pan_view": "right_drag",
            "zoom_view": "scroll"
        }
    },
    "current_mode": "default"
}
```

### 13.4 交互规范

#### 13.4.1 VTK 默认交互（current_mode: "default"）

| 操作               | 鼠标按键 | 行为           |
| ------------------ | -------- | -------------- |
| **旋转视图** | 左键拖动 | 相机绕焦点旋转 |
| **平移视图** | 中键拖动 | 移动相机位置   |
| **缩放视图** | 滚轮滚动 | 调整视场       |

#### 13.4.2 SolidWorks 风格交互（current_mode: "solidworks"）

**核心原则**：所有操作不改变模型几何，只改变观察视角。

| 操作               | 鼠标按键 | 行为                 | 说明         |
| ------------------ | -------- | -------------------- | ------------ |
| **旋转视图** | 中键拖动 | 相机绕模型中心旋转   | 改变观察角度 |
| **平移视图** | 右键拖动 | 移动相机位置         | 模型相对不动 |
| **缩放视图** | 滚轮滚动 | 以鼠标位置为中心缩放 | 调整视场     |

#### 13.4.3 模型交互（编辑模式）

**前提**：需先选中模型（编辑模式下左键单击）。

| 操作               | 鼠标按键 | 行为               | 说明         |
| ------------------ | -------- | ------------------ | ------------ |
| **选择模型** | 左键单击 | 选中模型           | 高亮显示     |
| **移动模型** | 左键拖动 | 沿平面移动         | 改变模型位置 |
| **旋转模型** | 右键拖动 | 自由旋转           | 改变模型方向 |
| **取消选择** | ESC      | 取消选中，恢复原色 | -            |
| **删除**     | Delete   | 删除选中实体       | -            |

#### 13.4.4 放置模式操作

| 操作           | 鼠标按键 | 行为             |
| -------------- | -------- | ---------------- |
| **预览** | 鼠标移动 | 预览模型跟随鼠标 |
| **放置** | 左键单击 | 确认放置位置     |
| **取消** | ESC      | 取消放置模式     |

### 13.5 坐标系与旋转方向

#### 13.5.1 坐标系定义

LSH 协议采用**右手坐标系**（建筑/BIM 风格，详见第 6 章）：

```
Z ↑ (高度/height)
  │
  │     ┌─────────┐
  │     │  空间   │
  │     │  Space  │
  │     └─────────┘
  │
  └──────────────────────→ X (宽度/width)
Y (深度/depth，向前)
```

| 轴          | 正方向 | 说明     | 对应尺寸      |
| ----------- | ------ | -------- | ------------- |
| **X** | 向右   | 水平方向 | width (宽度)  |
| **Y** | 向前   | 深度方向 | depth (深度)  |
| **Z** | 向上   | 高度方向 | height (高度) |

#### 13.5.2 旋转中心约定

**重要说明**：采用 **SolidWorks 模型旋转视角**，用户看到的是"模型在旋转"，而非"相机在旋转"。

**旋转中心**：**鼠标指向的位置**，不投影到地面。

```
┌─────────────────────────────────────────────────────────────┐
│                    旋转中心计算                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    1. 首先尝试拾取模型（vtkCellPicker）                     │
│    2. 如果拾取到模型，使用模型上的点                         │
│    3. 如果未拾取到模型，使用世界坐标拾取器（vtkWorldPointPicker）│
│                                                             │
│    注意：不投影到地面，使用实际的 3D 坐标                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 操作                   | 用户视角     | VTK API 调用             |
| ---------------------- | ------------ | ------------------------ |
| **鼠标向右拖动** | 元素向右旋转 | `camera.Azimuth(-dx)`  |
| **鼠标向上拖动** | 元素向上翻转 | `camera.Elevation(dy)` |

**实现要求**：

```python
# SolidWorks 模型旋转风格
# 1. 开始旋转时，拾取鼠标位置作为旋转中心
picker.Pick(mouse_x, mouse_y, 0, renderer)
rotation_center = picker.GetPickPosition()
camera.SetFocalPoint(rotation_center)

# 2. 旋转时，相机绕旋转中心旋转
# 鼠标向右拖动 → dx > 0 → 模型向右旋转 → 相机 Azimuth 负值
camera.Azimuth(-dx * factor)

# 鼠标向上拖动 → dy < 0 → 模型向上翻转 → 相机 Elevation 正值
camera.Elevation(dy * factor)

# 3. 结束旋转时，清理旋转中心状态
```

**视角对比**：

| 视角类型                         | 鼠标向右拖动 | 旋转中心         | 说明             |
| -------------------------------- | ------------ | ---------------- | ---------------- |
| **模型旋转（SolidWorks）** | 模型向右旋转 | 浮动（鼠标位置） | 用户感觉模型在动 |
| **相机旋转（VTK 默认）**   | 场景向左旋转 | 固定（场景原点） | 用户感觉视角在动 |

#### 13.5.3 实体旋转约定

| 操作               | 方向       | 角度变化 |
| ------------------ | ---------- | -------- |
| **向右拖动** | 顺时针旋转 | 角度增加 |
| **向左拖动** | 逆时针旋转 | 角度减少 |

**实现要求**：

```python
# 绕 Z 轴旋转
new_rotation = current_rotation + dx * factor
actor.SetOrientation(0, 0, new_rotation)
```

### 13.6 视觉反馈

#### 13.6.1 选中状态

| 状态             | 视觉效果                      |
| ---------------- | ----------------------------- |
| **未选中** | 原始颜色                      |
| **选中**   | 黄色高亮 (RGB: 1.0, 0.8, 0.0) |
| **拖动中** | 半透明 (Opacity: 0.7)         |

#### 13.6.2 放置预览

| 状态               | 视觉效果                                |
| ------------------ | --------------------------------------- |
| **预览中**   | 半透明绿色 (Opacity: 0.5, Color: green) |
| **可放置**   | 预览正常显示                            |
| **不可放置** | 预览显示红色                            |

### 13.7 交互事件

#### 13.7.1 交互状态事件

| 事件类型                     | 值                           | 携带数据                    | 说明         |
| ---------------------------- | ---------------------------- | --------------------------- | ------------ |
| `INTERACTION_MODE_CHANGED` | `interaction_mode_changed` | extra.{mode, previous_mode} | 交互模式变化 |
| `ELEMENT_SELECTED`         | `element_selected`         | target_id, position         | 元素被选中   |
| `ELEMENT_DESELECTED`       | `element_deselected`       | target_id                   | 元素取消选中 |
| `ELEMENT_DRAG_START`       | `element_drag_start`       | target_id, position         | 开始拖动元素 |
| `ELEMENT_DRAG_END`         | `element_drag_end`         | target_id, position         | 结束拖动元素 |
| `ELEMENT_ROTATE_START`     | `element_rotate_start`     | target_id, rotation         | 开始旋转元素 |
| `ELEMENT_ROTATE_END`       | `element_rotate_end`       | target_id, rotation         | 结束旋转元素 |

#### 13.7.2 相机事件

| 事件类型                | 值                      | 携带数据                   | 说明                                       |
| ----------------------- | ----------------------- | -------------------------- | ------------------------------------------ |
| `CAMERA_ROTATED`      | `camera_rotated`      | extra.{azimuth, elevation} | 相机旋转                                   |
| `CAMERA_PANNED`       | `camera_panned`       | position (focal_point)     | 相机平移                                   |
| `CAMERA_ZOOMED`       | `camera_zoomed`       | extra.{factor, position}   | 相机缩放                                   |
| `CAMERA_VIEW_CHANGED` | `camera_view_changed` | extra.view_type            | 相机视角切换（top/front/side/perspective） |

### 13.8 实现参考

#### 13.8.1 相机旋转实现

```python
def rotate_camera(self, dx: float, dy: float):
    """相机旋转
  
    Args:
        dx: 鼠标水平移动距离（正值=向右）
        dy: 鼠标垂直移动距离（正值=向下）
    """
    camera = self._renderer.GetActiveCamera()
  
    # 水平旋转：鼠标向右 → 场景向右旋转
    camera.Azimuth(dx * 0.5)
  
    # 垂直旋转：鼠标向上 → 相机向上看
    camera.Elevation(-dy * 0.5)
  
    # 防止翻转：检查 ViewUp 方向
    view_up = camera.GetViewUp()
    if view_up[2] < 0:
        camera.SetViewUp(-view_up[0], -view_up[1], abs(view_up[2]))
  
    self._render()
```

#### 13.8.2 实体拖动实现

```python
def drag_element(self, screen_x: float, screen_y: float):
    """拖动实体
  
    Args:
        screen_x: 屏幕坐标 X
        screen_y: 屏幕坐标 Y
    """
    if not self._selected_actor:
        return
  
    # 拾取世界坐标
    self._picker.Pick(screen_x, screen_y, 0, self._renderer)
    pick_pos = self._picker.GetPickPosition()
  
    # 计算新位置（保持 Z 轴不变）
    new_x = pick_pos[0] + self._drag_offset[0]
    new_y = pick_pos[1] + self._drag_offset[1]
    new_z = self._selected_actor.GetPosition()[2]
  
    # 边界限制
    if self._layout and hasattr(self._layout, 'scene_bounds'):
        clamped = self._layout.scene_bounds.clamp(new_x, new_y, new_z)
        new_x, new_y, new_z = clamped
  
    self._selected_actor.SetPosition(new_x, new_y, new_z)
    self._render()
```

### 13.9 兼容性说明

| 渲染引擎           | 相机 API                                     | 实体 API                                            | 拾取 API                         |
| ------------------ | -------------------------------------------- | --------------------------------------------------- | -------------------------------- |
| **VTK**      | `camera.Azimuth()`, `camera.Elevation()` | `actor.SetPosition()`, `actor.SetOrientation()` | `vtkPropPicker.Pick()`         |
| **Three.js** | `camera.rotation.y`, `camera.rotation.x` | `mesh.position`, `mesh.rotation`                | `raycaster.intersectObjects()` |
| **Unity**    | `transform.Rotate()`                       | `transform.position`, `transform.rotation`      | `Physics.Raycast()`            |

---

## 14. 版本历史 (Version History)

| 版本  | 日期       | 变更内容                                                                                                                                                                                                                                  |
| ----- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3.0.2 | 2026-03-08 | **属性定义系统**：新增 `ELEMENT_PROPERTY_DEFINITIONS` 配置，支持声明式定义元素属性（编辑、展示、类型）；新增 `PropertyDefinition` 数据类；规范类型判断应从 `element.category` 自动获取，不作为参数传入 |
| 3.0.1 | 2026-03-08 | **协议定位升级**：从"视图同步协议"升级为"虚拟现实统一协议"；完善 CATEGORY_DEFAULTS 配置；添加 `is_space()`、`is_toggleable()`、`is_movable()`、`is_custom_model()` 便捷方法；更新所有方法签名为 `category: str` |
| 3.0.0 | 2026-03-07 | **核心概念简化**：从四要素（空间、实体、关系、属性）简化为三要素（元素、关系、属性）；移除 SPACE/ENTITY 类型区分，统一为 Element；新增属性查询机制（category 默认配置 + extra 覆盖） |
| 2.6.0 | 2026-03-06 | **事件溯源架构**：定义事件溯源接口，支持时间旅行和状态回滚；新增 EventSourcingManager 管理器；完善路径规划适配新 LSH 架构 |
| 2.5.0 | 2026-03-04 | **分层架构设计**：新增分层架构设计章节，定义 Model/ActorFactory/View 三层分离架构；确立"数据与渲染彻底分离"核心理念；明确层级职责、设计原则、禁止行为；口诀"Model定长相，Factory转演员，Render只管上场" |
| 2.4.0 | 2026-03-04 | **内外坐标系分离架构**：新增架构规范章节，明确"输入数据使用LSH、输出数据使用LSH、内部渲染层转换"原则；定义架构规则、实现示例、禁止行为；确保系统对外统一使用LSH坐标系，内部渲染层透明转换 |
| 2.3.0 | 2026-03-04 | **3D 引擎坐标转换规范**：新增 3D 引擎坐标转换规范章节，定义 LSH/Godot/VTK/Blender 坐标系转换规则；统一 Python 端转换，避免各引擎重复实现；采用建筑/BIM 风格坐标系（X=右, Y=前, Z=上）                                               |
| 2.2.0 | 2026-03-03 | **路径规划增强**：新增途径点事件、覆盖模式事件、避障配置事件；定义 PathPlanningConfig 数据结构和交互流程 |
| 2.1.0 | 2026-03-03 | **交互协议**：新增交互协议章节，定义鼠标交互规范、坐标系与旋转方向、视觉反馈、交互事件 |
| 2.0.0 | 2026-03-02 | **重大重构**：协议定位为虚拟世界通用协议；ElementType 简化为 SPACE/ENTITY；业务分类通过 category 实现 |
| 1.0.0 | 2026-02-28 | **初始版本**：发布-订阅模式、位置优先、坐标系统规范 |

---

## 15. 未来规划 (Roadmap)

### 15.1 v3.1.0 计划

- [ ] **跨语言 SDK**：JavaScript/TypeScript 支持
- [ ] **现实世界适配器**：IoT 设备、传感器数据接入

### 15.2 v3.2.0 计划

- [ ] **性能优化**：大规模场景渲染优化
- [ ] **持久化层**：元素状态存储与恢复

### 15.3 v4.0.0 愿景

- [ ] **分布式支持**：跨进程、跨设备同步
- [ ] **冲突解决**：CRDT 集成，支持多人协作
- [ ] **标准化**：提交为开放标准
- [ ] **生态建设**：支持 Unity、Unreal Engine

---

## 附录 A：迁移指南 (Migration Guide)

### 从 v2.x 迁移到 v3.0

#### 核心概念变更

| v2.x 概念 | v3.0 概念 | 说明 |
|-----------|-----------|------|
| SPACE/ENTITY | Element | 不再区分类型，统一为元素 |
| element_type | category | 业务分类替代协议类型 |
| 能力属性 | 属性查询机制 | 通过 get_property() 获取 |

#### 代码迁移示例

```python
# v2.x：使用 element_type
if element.element_type == ElementType.SPACE:
    # 空间逻辑
    pass

# v3.0：使用属性查询
if element.is_space():
    # 空间逻辑
    pass

# v2.x：直接访问能力属性
if element.can_contain:
    pass

# v3.0：通过属性查询
if element.get_property("can_contain", False):
    pass
```

#### ElementType 变更

| v1.x              | v2.x element_type | v3.0 category       |
| ----------------- | ----------------- | ------------------- |
| `ROOM`          | `SPACE`         | `"room"`          |
| `DEVICE`        | `ENTITY`        | `"device"`        |
| `ITEM`          | `ENTITY`        | `"item"`          |
| `CUSTOM_MODEL`  | `ENTITY`        | `"custom_model"`  |
| `FURNITURE`     | `ENTITY`        | `"furniture"`     |
| `ROBOT`         | `ENTITY`        | `"robot"`         |
| `MODULE`        | `ENTITY`        | `"module"`        |
| `WALL`          | `ENTITY`        | `"wall"`          |
| `FLOOR_ELEMENT` | `ENTITY`        | `"floor_element"` |
| `PATH`          | `ENTITY`        | `"path"`          |

#### 事件类型变更

| v1.x                        | v2.0                                                    |
| --------------------------- | ------------------------------------------------------- |
| `ROOM_ADDED`              | `ELEMENT_ADDED` + `category="room"`                 |
| `ROOM_DELETED`            | `ELEMENT_DELETED` + `category="room"`               |
| `ROOM_POSITION_CHANGED`   | `ELEMENT_POSITION_CHANGED` + `target_type="space"`  |
| `ROOM_SIZE_CHANGED`       | `ELEMENT_CHANGED` + `category="room"`               |
| `DEVICE_ADDED`            | `ELEMENT_ADDED` + `category="device"`               |
| `DEVICE_DELETED`          | `ELEMENT_DELETED` + `category="device"`             |
| `DEVICE_POSITION_CHANGED` | `ELEMENT_POSITION_CHANGED` + `target_type="entity"` |
| `DEVICE_STATE_CHANGED`    | `ELEMENT_CHANGED` + `category="device"`             |
| `DEVICE_ROOM_CHANGED`     | `ELEMENT_HIERARCHY_CHANGED`                           |
| `ITEM_*`                  | `ELEMENT_*` + `category="item"`                     |
| `CUSTOM_MODEL_*`          | `ELEMENT_*` + `category="custom_model"`             |
| `ROBOT_*`                 | `ELEMENT_*` + `category="robot"`                    |
| `MODEL_INSTANCE_*`        | `ELEMENT_*` + `category="model_instance"`           |

#### 代码迁移示例

```python
# v1.x
view_sync.publish_room_position_changed("room_001", 2.0, 3.0, 0)

# v3.0
view_sync.publish_element_position_changed("room_001", "room", 2.0, 3.0, 0)
```

```python
# v1.x
view_sync.publish_device_state_changed("device_001", DeviceState.ON)

# v3.0
element = SceneElement.create(
    id="device_001",
    name="智能灯",
    category="device",
    extra={"state": "on"}
)
view_sync.publish_element_changed(element)
```

```python
# v1.x 订阅
view_sync.subscribe(ViewSyncEvents.ROOM_POSITION_CHANGED, on_room_moved)
view_sync.subscribe(ViewSyncEvents.DEVICE_POSITION_CHANGED, on_device_moved)

# v3.0 订阅（统一处理）
view_sync.subscribe(ViewSyncEvents.ELEMENT_POSITION_CHANGED, on_position_changed)

def on_position_changed(event):
    category = event.target_type  # 现在存储 category
    # 根据 category 分别处理
```
