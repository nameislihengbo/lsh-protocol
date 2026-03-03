# LSH 视图同步协议

**Li Shi Hang View Synchronization Protocol**

| 属性 | 值 |
|------|-----|
| 版本 | 2.2.0 |
| 状态 | 正式版 (Release) |
| 作者 | 李恒波 (Li Hengbo) |
| 日期 | 2026-03-02 |
| 许可证 | MIT |

---

## 1. 摘要 (Abstract)

LSH 协议是一种面向虚拟世界的视图同步协议，定义了空间数据的标准化表示和同步机制。该协议定义了一套标准的事件类型和数据结构，用于在多视图（结构视图、2D 视图、3D 视图、列表视图）之间保持数据一致性。

协议的核心思想是"**位置优先**"——所有事件都携带位置信息，使得空间变化能够自动同步到所有相关视图。

**v2.0.0 重大更新**：
- **协议重新定位**：从智能家居升级为虚拟世界通用协议
- **核心类型简化**：`ElementType` 仅保留 `SPACE`（空间）和 `ENTITY`（实体）两种核心类型
- **业务分类解耦**：通过 `category` 字段实现业务分类，不再绑定特定领域
- **事件系统精简**：统一使用 `ELEMENT_*` 事件，移除所有领域特定事件

---

## 2. 应用场景

**应用场景**：

| 场景层级 | 说明 | 典型应用 |
|------|------|------|
| **家庭** | 智能家居、物品管理 | 房间、设备、家具的可视化管理 |
| **社区** | 社区管理与服务 | 门禁、停车、公共设施、环境监测 |
| **城市** | 城市级应用 | 交通管理、城市安防、公共服务 |
| **国家** | 跨区域协调 | 物流网络、能源调度、应急响应 |
| **世界** | 全球虚拟世界 | 元宇宙、跨国协作、全球模拟 |

**场景延伸路线**：家庭 → 社区 → 城市 → 国家 → 世界

---

## 3. 核心概念 (Core Concepts)

### 3.1 虚拟世界模型

LSH 协议将虚拟世界抽象为四个核心要素：

```
┌─────────────────────────────────────────────────────┐
│                    虚拟世界                          │
├─────────────────────────────────────────────────────┤
│  空间 (Space)   │ 有边界、可包含其他元素        │
│  实体 (Entity)  │ 可交互、有行为               │
│  关系 (Relation)│ 层级、父子、包含              │
│  属性 (Property)│ 位置、旋转、缩放、可见性      │
└─────────────────────────────────────────────────────┘
```

### 3.2 空间与实体

| 特性 | Space (空间) | Entity (实体) |
|------|-------------|---------------|
| 边界 | ✅ 必须有 | ❌ 可选 |
| 可包含 | ✅ 可包含 Space 和 Entity | ⚠️ 仅可包含 Entity（组件） |
| 坐标系 | ✅ 定义本地坐标系 | ❌ 使用父级坐标系 |
| 典型例子 | 房间、楼层、区域、地图区块 | 设备、家具、角色、道具 |

### 3.3 术语对照

| 协议层（抽象） | 渲染层（VTK） | 说明 |
|--------------|--------------|------|
| **Element（元素）** | **Actor** | 场景中的对象 |
| Space（空间） | 多个 Actor | 房间 = 墙壁 + 地板 + 天花板 |
| Entity（实体） | 1 个 Actor | 设备、家具等 |

**注意**：协议使用 Element 作为抽象概念，渲染引擎实现时映射到具体的可视化对象（如 VTK 的 Actor）。

### 1.3 业务分类

业务类型通过 `category` 字段实现，用户可自定义：

| category | 说明 | element_type |
|----------|------|--------------|
| `room` | 房间 | SPACE |
| `floor` | 楼层 | SPACE |
| `zone` | 区域 | SPACE |
| `device` | 设备 | ENTITY |
| `furniture` | 家具 | ENTITY |
| `robot` | 机器人 | ENTITY |
| `character` | 角色 | ENTITY |
| `prop` | 道具 | ENTITY |
| `...` | 用户自定义 | SPACE/ENTITY |

---

## 4. 动机 (Motivation)

### 4.1 问题背景

在虚拟世界可视化系统中，同一数据需要在多个视图中展示：

| 视图类型 | 展示形式 | 数据维度 |
|---------|---------|---------|
| 结构视图 | 树形列表 | 层级关系 |
| 2D 视图 | 平面图标 | (x, y) |
| 3D 视图 | 立体模型 | (x, y, z) |
| 列表视图 | 表格行 | 状态信息 |

传统做法是在数据变化时手动调用各视图的更新方法，存在以下问题：

1. **耦合度高**：数据层需要知道所有视图的存在
2. **易遗漏**：新增视图时容易忘记添加更新调用
3. **不一致**：不同操作的更新逻辑分散，难以维护

### 4.2 解决方案

LSH 协议采用**发布-订阅模式**，将数据变化抽象为事件：

```
数据变化 → 发布事件 → 所有订阅者自动响应
```

视图只需订阅自己关心的事件，无需知道数据来源，实现完全解耦。

---

## 5. 术语定义 (Terminology)

| 术语 | 定义 |
|------|------|
| **事件 (Event)** | 数据变化的抽象表示，包含事件类型、目标 ID、位置信息等 |
| **发布者 (Publisher)** | 产生事件的组件，通常是数据操作层 |
| **订阅者 (Subscriber)** | 接收并响应事件的组件，通常是视图层 |
| **位置数据 (PositionData)** | 三维空间坐标，包含 x、y、z 分量 |
| **尺寸数据 (SizeData)** | 三维尺寸，包含 width、depth、height 分量 |
| **批量模式 (Batch Mode)** | 事件合并模式，多个事件合并为一次更新 |
| **空间 (Space)** | 有边界的容器，可包含其他空间和实体 |
| **实体 (Entity)** | 场景中的可交互对象 |

---

## 6. 坐标系统 (Coordinate System)

### 6.1 统一坐标系

LSH 协议采用**右手坐标系**，所有视图必须遵循统一的坐标系统：

```
Y ↑
  │
  │     ┌─────────┐
  │     │  空间   │
  │     │  Space  │
  │     └─────────┘
  │
  └──────────────────────→ X
Z (向上，垂直于屏幕)
```

| 轴 | 方向 | 说明 |
|----|------|------|
| **X 轴** | 向右为正 | 水平方向 |
| **Y 轴** | 向上为正 | 垂直方向 |
| **Z 轴** | 向上为正 | 高度方向（3D） |

### 6.2 视图坐标适配

| 视图 | 原始坐标系 | 适配方式 |
|------|-----------|---------|
| **2D 视图 (Qt)** | Y 轴向下 | `scale(1, -1)` 翻转 Y 轴 |
| **3D 视图 (VTK)** | Y 轴向上 | 无需适配 |
| **结构视图** | 无坐标 | 不涉及 |

### 6.3 文字标签处理

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

### 6.4 坐标转换

```python
# 2D 视图坐标 → 统一坐标系
def to_unified_coords(x: float, y: float, space_height: float) -> PositionData:
    return PositionData(x=x, y=space_height - y, z=0.0)

# 统一坐标系 → 2D 视图坐标
def to_2d_coords(pos: PositionData, space_height: float) -> tuple:
    return (pos.x, space_height - pos.y)
```

---

## 7. 数据结构 (Data Structures)

### 7.1 位置数据 (PositionData)

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

### 7.2 尺寸数据 (SizeData)

```python
@dataclass
class SizeData:
    """三维尺寸"""
    width: float = 1.0   # 宽度（米）
    depth: float = 1.0   # 深度（米）
    height: float = 1.0  # 高度（米）
    
    def to_dict(self) -> Dict[str, float]:
        return {"width": self.width, "depth": self.depth, "height": self.height}
```

### 7.3 边界数据 (Bounds)

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
    def center(self) -> Tuple[float, float, float]:
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

### 7.4 事件数据 (ViewSyncEvent)

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

### 7.5 场景元素 (SceneElement)

```python
class ElementType(Enum):
    """元素类型（协议层）
    
    LSH 协议仅定义两种核心类型：
    - SPACE: 空间，有边界，可包含其他元素
    - ENTITY: 实体，可交互，有行为
    
    业务分类通过 category 字段实现。
    """
    SPACE = "space"
    ENTITY = "entity"


@dataclass
class SceneElement:
    """统一的场景元素模型
    
    所有场景中的可见元素都使用此模型，便于：
    1. 统一搜索
    2. 跨视图高亮
    3. LSH 同步
    """
    id: str                              # 元素唯一标识
    name: str                            # 元素名称
    element_type: ElementType            # 元素类型（SPACE/ENTITY）
    
    # 变换属性
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: float = 1.0
    
    # 尺寸信息
    size: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    
    # 边界（SPACE 必须有）
    bounds: Optional[Bounds] = None
    
    # 层级关系
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # 业务分类（用户自定义）
    category: str = ""
    tags: List[str] = field(default_factory=list)
    
    # 扩展数据
    extra: Dict[str, Any] = field(default_factory=dict)
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 可见性
    visible: bool = True
    searchable: bool = True
```

### 7.6 元素注册表 (SceneElementRegistry)

```python
class SceneElementRegistry:
    """场景元素注册表
    
    统一管理所有场景元素，支持：
    1. 注册/注销元素
    2. 按类型/分类/标签搜索
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
    
    def get_spaces(self) -> List[SceneElement]:
        """获取所有空间"""
        pass
    
    def get_entities(self) -> List[SceneElement]:
        """获取所有实体"""
        pass
    
    def get_by_type(self, element_type: ElementType) -> List[SceneElement]:
        """按类型获取元素"""
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
                                 new_position: Tuple[float, float, float]) -> None:
        """级联更新位置（父元素移动时自动更新子元素）"""
        pass
```

---

## 8. 事件类型 (Event Types)

### 8.1 统一元素事件

LSH 协议 v2.0.0 统一使用 `ELEMENT_*` 事件，通过 `target_type` 区分 SPACE/ENTITY，通过 `extra.category` 区分业务类型：

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `ELEMENT_ADDED` | `element_added` | position, size, extra | 元素添加 |
| `ELEMENT_DELETED` | `element_deleted` | extra | 元素删除 |
| `ELEMENT_CHANGED` | `element_changed` | position, size, extra | 元素属性变化 |
| `ELEMENT_POSITION_CHANGED` | `element_position_changed` | position | 元素位置变化 |
| `ELEMENT_VISIBILITY_CHANGED` | `element_visibility_changed` | extra.visible | 元素可见性变化 |
| `ELEMENT_HIERARCHY_CHANGED` | `element_hierarchy_changed` | parent_id, extra | 元素层级关系变化 |
| `ELEMENTS_SYNC` | `elements_sync` | extra.elements | 批量同步所有元素 |

### 8.2 场景事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `SCENE_ACTIVATED` | `scene_activated` | extra.scene_id | 场景激活 |
| `SCENE_CHANGED` | `scene_changed` | extra | 场景变化 |
| `SCENE_BOUNDS_CHANGED` | `scene_bounds_changed` | extra.{min_x, max_x, min_y, max_y, min_z, max_z} | 场景边界变化 |

### 8.3 编辑模式事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `EDIT_MODE_CHANGED` | `edit_mode_changed` | extra.enabled | 编辑模式切换 |

### 8.4 路径规划事件

#### 8.4.1 基础路径事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `PATH_CALCULATED` | `path_calculated` | extra.{path, distance, estimated_time, waypoints} | 路径计算完成 |
| `PATH_VISUALIZED` | `path_visualized` | extra.{path, view_type, color, clear_previous} | 路径可视化 |
| `PATH_EXECUTED` | `path_executed` | extra.{success, message} | 路径执行完成 |
| `NAVIGATION_MAP_UPDATED` | `navigation_map_updated` | extra.{grid_info} | 导航地图更新 |

#### 8.4.2 路径选择事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `PATH_START_SELECTED` | `path_start_selected` | position, target_id (element_id) | 路径起点选择 |
| `PATH_END_SELECTED` | `path_end_selected` | position, target_id (element_id) | 路径终点选择 |
| `PATH_WAYPOINT_ADDED` | `path_waypoint_added` | position, target_id, extra.{index} | 添加途径点 |
| `PATH_WAYPOINT_REMOVED` | `path_waypoint_removed` | position, target_id, extra.{index} | 移除途径点 |
| `PATH_WAYPOINTS_CLEARED` | `path_waypoints_cleared` | - | 清除所有途径点 |
| `PATH_SELECTION_MODE_CHANGED` | `path_selection_mode_changed` | extra.mode | 路径选择模式变化 |
| `PATH_SELECTION_CLEARED` | `path_selection_cleared` | - | 路径选择清除 |

#### 8.4.3 路径规划模式事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `PATH_PLANNING_MODE_CHANGED` | `path_planning_mode_changed` | extra.{mode, config} | 路径规划模式变化 |
| `PATH_OBSTACLE_AVOIDANCE_CHANGED` | `path_obstacle_avoidance_changed` | extra.{enabled, obstacles} | 避障设置变化 |
| `PATH_COVERAGE_MODE_CHANGED` | `path_coverage_mode_changed` | extra.{enabled, algorithm, area_bounds} | 覆盖模式设置变化 |
| `PATH_COVERAGE_PROGRESS` | `path_coverage_progress` | extra.{progress, covered_area, total_area} | 覆盖进度更新 |
| `PATH_COVERAGE_COMPLETED` | `path_coverage_completed` | extra.{success, coverage_rate, path} | 覆盖完成 |

### 8.5 路径规划数据结构

#### 8.5.1 路径规划配置

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

#### 8.5.2 路径规划模式

```python
class PathPlanningMode(Enum):
    """路径规划模式"""
    NORMAL = "normal"                  # 普通模式：起点→终点
    WITH_WAYPOINTS = "waypoints"       # 途径点模式：起点→途径点→终点
    COVERAGE = "coverage"              # 覆盖模式：全覆盖路径（扫地机器人）
    OBSTACLE_AVOIDANCE = "avoidance"   # 避障模式：动态避障
```

#### 8.5.3 覆盖路径结果

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

### 8.6 路径规划交互流程

#### 8.6.1 普通路径规划流程

```
1. 点击"路径规划"按钮 → 进入路径选择模式
2. 选择起点元素 → 发布 PATH_START_SELECTED 事件
3. 选择终点元素 → 发布 PATH_END_SELECTED 事件
4. （可选）配置避障 → 发布 PATH_OBSTACLE_AVOIDANCE_CHANGED 事件
5. 执行路径规划 → 发布 PATH_CALCULATED 事件
6. 可视化路径 → 发布 PATH_VISUALIZED 事件
```

#### 8.6.2 途径点路径规划流程

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

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `MODEL_TEMPLATE_ADDED` | `model_template_added` | extra.{template_data} | 模型模板添加 |
| `MODEL_TEMPLATE_UPDATED` | `model_template_updated` | extra.{template_data} | 模型模板更新 |
| `MODEL_TEMPLATE_REMOVED` | `model_template_removed` | target_id | 模型模板移除 |

### 8.8 全局事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `LAYOUT_LOADED` | `layout_loaded` | - | 布局加载完成 |
| `LAYOUT_CHANGED` | `layout_changed` | - | 布局变化 |
| `LAYOUT_CENTERED` | `layout_centered` | position (offset_x, offset_y, offset_z) | 布局居中（整体移动） |
| `FULL_REFRESH` | `full_refresh` | - | 全量刷新 |

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
        element: 场景元素对象
    """
    pass

def publish_element_deleted(self, element_id: str, element_type: ElementType, 
                            extra: dict = None) -> None:
    """发布元素删除事件"""
    pass

def publish_element_changed(self, element: SceneElement, changes: dict = None) -> None:
    """发布元素变化事件"""
    pass

def publish_element_position_changed(self, element_id: str, element_type: ElementType,
                                     x: float, y: float, z: float = 0.0) -> None:
    """发布元素位置变化事件"""
    pass

def publish_element_visibility_changed(self, element_id: str, element_type: ElementType,
                                       visible: bool) -> None:
    """发布元素可见性变化事件"""
    pass

def publish_element_hierarchy_changed(self, element_id: str, element_type: ElementType,
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

### 10.1 创建空间和实体

```python
from src.home3d.view_sync import view_sync, ViewSyncEvents
from src.home3d.models.scene_element import SceneElement, ElementType

# 创建空间元素
room = SceneElement.create_space(
    id="room_001", 
    name="客厅", 
    position=(0, 0, 0),
    size=(5.0, 4.0, 2.8),
    category="room"
)

# 创建实体元素
device = SceneElement.create_entity(
    id="device_001",
    name="智能灯",
    position=(2.5, 2.0, 1.5),
    category="device",
    parent_id="room_001"
)

# 发布元素添加事件
view_sync.publish_element_added(room)
view_sync.publish_element_added(device)
```

### 10.2 视图订阅事件

```python
class VTK3DView:
    def __init__(self):
        # 订阅统一元素事件
        view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, 
                           self._on_element_added)
        view_sync.subscribe(ViewSyncEvents.ELEMENT_POSITION_CHANGED, 
                           self._on_position_changed)
        view_sync.subscribe(ViewSyncEvents.ELEMENT_DELETED, 
                           self._on_element_deleted)
    
    def _on_element_added(self, event: ViewSyncEvent):
        """响应元素添加"""
        category = event.extra.get("category", "")
        if category == "room":
            self._add_room(event.target_id, event.position, event.size)
        elif category == "device":
            self._add_device(event.target_id, event.position)
    
    def _on_position_changed(self, event: ViewSyncEvent):
        """响应位置变化"""
        target_type = event.target_type  # "space" 或 "entity"
        self._update_position(event.target_id, event.position)
    
    def _on_element_deleted(self, event: ViewSyncEvent):
        """响应元素删除"""
        category = event.extra.get("category", "")
        if category == "custom_model":
            delete_file = event.extra.get("delete_file", False)
            self._remove_model(event.target_id, delete_file)
```

### 10.3 批量更新

```python
# 批量更新时合并事件，避免重复刷新
view_sync.batch_begin()
view_sync.publish_element_position_changed("room_001", ElementType.SPACE, 2.0, 3.0, 0)
view_sync.publish_element_position_changed("room_001", ElementType.SPACE, 2.5, 3.5, 0)  # 会被合并
view_sync.publish_element_position_changed("device_001", ElementType.ENTITY, 1.0, 1.0, 1.5)
view_sync.batch_end()  # 只触发两次刷新（room_001 和 device_001）
```

### 10.4 层级关系变化

```python
# 将设备从一个房间移动到另一个房间
view_sync.publish_element_hierarchy_changed(
    element_id="device_001",
    element_type=ElementType.ENTITY,
    old_parent_id="room_001",
    new_parent_id="room_002"
)
```

### 10.5 元素搜索

```python
from src.home3d.models.scene_element import SceneElementRegistry

registry = SceneElementRegistry()

# 注册元素
registry.register(room)
registry.register(device)

# 按类型搜索
spaces = registry.get_spaces()
entities = registry.get_entities()

# 按分类搜索
devices = registry.get_by_category("device")

# 按标签搜索
tagged = registry.get_by_tag("smart")

# 关键词搜索
results = registry.search("灯", categories=["device"])
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

| 协议 | 领域 | 位置支持 | 空间语义 | 批量优化 | 类型系统 |
|------|------|---------|---------|---------|---------|
| **LSH** | 虚拟世界 | ✅ 原生 | ✅ 原生 | ✅ | 灵活（SPACE/ENTITY + category） |
| 观察者模式 | 通用 | ❌ | ❌ | ❌ | 无 |
| Redux/Flux | 前端状态管理 | ❌ | ❌ | ❌ | 无 |
| MQTT | 物联网通信 | ❌ | ❌ | ❌ | 无 |
| OPC UA | 工业自动化 | ❌ | ❌ | ❌ | 强类型 |
| CRDT | 分布式协作 | ❌ | ❌ | ✅ | 无 |

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

| 用户视角 | 实际操作 | 说明 |
|---------|---------|------|
| "旋转视图" | 旋转模型 | 模型绕旋转中心旋转 |
| "平移视图" | 平移模型 | 模型在屏幕上移动 |
| "缩放视图" | 移动相机 | 相机靠近/远离模型 |

### 13.2 设计原则

LSH 交互协议定义了 3D 视图中的标准交互方式，遵循以下原则：

| 原则 | 说明 |
|------|------|
| **模型为中心** | 用户操作的是模型，相机只是观察者 |
| **相机与实体分离** | 相机操作和实体操作使用不同的鼠标按键，互不干扰 |
| **一致性** | 所有实现必须遵循统一的交互规则 |
| **直觉性** | 交互方向与视觉反馈一致，符合用户直觉 |
| **可扩展** | 支持自定义交互模式 |

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

| 操作 | 鼠标按键 | 行为 |
|------|---------|------|
| **旋转视图** | 左键拖动 | 相机绕焦点旋转 |
| **平移视图** | 中键拖动 | 移动相机位置 |
| **缩放视图** | 滚轮滚动 | 调整视场 |

#### 13.4.2 SolidWorks 风格交互（current_mode: "solidworks"）

**核心原则**：所有操作不改变模型几何，只改变观察视角。

| 操作 | 鼠标按键 | 行为 | 说明 |
|------|---------|------|------|
| **旋转视图** | 中键拖动 | 相机绕模型中心旋转 | 改变观察角度 |
| **平移视图** | 右键拖动 | 移动相机位置 | 模型相对不动 |
| **缩放视图** | 滚轮滚动 | 以鼠标位置为中心缩放 | 调整视场 |

#### 13.4.3 模型交互（编辑模式）

**前提**：需先选中模型（编辑模式下左键单击）。

| 操作 | 鼠标按键 | 行为 | 说明 |
|------|---------|------|------|
| **选择模型** | 左键单击 | 选中模型 | 高亮显示 |
| **移动模型** | 左键拖动 | 沿平面移动 | 改变模型位置 |
| **旋转模型** | 右键拖动 | 自由旋转 | 改变模型方向 |
| **取消选择** | ESC | 取消选中，恢复原色 | - |
| **删除** | Delete | 删除选中实体 | - |

#### 13.3.3 放置模式操作

| 操作 | 鼠标按键 | 行为 |
|------|---------|------|
| **预览** | 鼠标移动 | 预览模型跟随鼠标 |
| **放置** | 左键单击 | 确认放置位置 |
| **取消** | ESC | 取消放置模式 |

### 13.4 坐标系与旋转方向

#### 13.4.1 坐标系定义

```
Y ↑ (向前)
  │
  │     ┌─────────┐
  │     │  空间   │
  │     │  Space  │
  │     └─────────┘
  │
  └──────────────────────→ X (向右)
Z ↑ (向上，垂直于屏幕)
```

| 轴 | 正方向 | 说明 |
|----|--------|------|
| **X** | 向右 | 水平方向 |
| **Y** | 向前 | 深度方向 |
| **Z** | 向上 | 高度方向 |

#### 13.4.2 旋转中心约定

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

| 操作 | 用户视角 | VTK API 调用 |
|------|---------|-------------|
| **鼠标向右拖动** | 元素向右旋转 | `camera.Azimuth(-dx)` |
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

| 视角类型 | 鼠标向右拖动 | 旋转中心 | 说明 |
|---------|-------------|---------|------|
| **模型旋转（SolidWorks）** | 模型向右旋转 | 浮动（鼠标位置） | 用户感觉模型在动 |
| **相机旋转（VTK 默认）** | 场景向左旋转 | 固定（场景原点） | 用户感觉视角在动 |

#### 13.4.3 实体旋转约定

| 操作 | 方向 | 角度变化 |
|------|------|---------|
| **向右拖动** | 顺时针旋转 | 角度增加 |
| **向左拖动** | 逆时针旋转 | 角度减少 |

**实现要求**：
```python
# 绕 Z 轴旋转
new_rotation = current_rotation + dx * factor
actor.SetOrientation(0, 0, new_rotation)
```

### 13.5 视觉反馈

#### 13.5.1 选中状态

| 状态 | 视觉效果 |
|------|---------|
| **未选中** | 原始颜色 |
| **选中** | 黄色高亮 (RGB: 1.0, 0.8, 0.0) |
| **拖动中** | 半透明 (Opacity: 0.7) |

#### 13.5.2 放置预览

| 状态 | 视觉效果 |
|------|---------|
| **预览中** | 半透明绿色 (Opacity: 0.5, Color: green) |
| **可放置** | 预览正常显示 |
| **不可放置** | 预览显示红色 |

### 13.6 交互事件

#### 13.6.1 交互状态事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `INTERACTION_MODE_CHANGED` | `interaction_mode_changed` | extra.{mode, previous_mode} | 交互模式变化 |
| `ELEMENT_SELECTED` | `element_selected` | target_id, position | 元素被选中 |
| `ELEMENT_DESELECTED` | `element_deselected` | target_id | 元素取消选中 |
| `ELEMENT_DRAG_START` | `element_drag_start` | target_id, position | 开始拖动元素 |
| `ELEMENT_DRAG_END` | `element_drag_end` | target_id, position | 结束拖动元素 |
| `ELEMENT_ROTATE_START` | `element_rotate_start` | target_id, rotation | 开始旋转元素 |
| `ELEMENT_ROTATE_END` | `element_rotate_end` | target_id, rotation | 结束旋转元素 |

#### 13.6.2 相机事件

| 事件类型 | 值 | 携带数据 | 说明 |
|---------|-----|---------|------|
| `CAMERA_ROTATED` | `camera_rotated` | extra.{azimuth, elevation} | 相机旋转 |
| `CAMERA_PANNED` | `camera_panned` | position (focal_point) | 相机平移 |
| `CAMERA_ZOOMED` | `camera_zoomed` | extra.{factor, position} | 相机缩放 |
| `CAMERA_VIEW_CHANGED` | `camera_view_changed` | extra.view_type | 相机视角切换（top/front/side/perspective） |

### 13.7 实现参考

#### 13.7.1 相机旋转实现

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

#### 13.7.2 实体拖动实现

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

### 13.8 兼容性说明

| 渲染引擎 | 相机 API | 实体 API | 拾取 API |
|---------|---------|---------|---------|
| **VTK** | `camera.Azimuth()`, `camera.Elevation()` | `actor.SetPosition()`, `actor.SetOrientation()` | `vtkPropPicker.Pick()` |
| **Three.js** | `camera.rotation.y`, `camera.rotation.x` | `mesh.position`, `mesh.rotation` | `raycaster.intersectObjects()` |
| **Unity** | `transform.Rotate()` | `transform.position`, `transform.rotation` | `Physics.Raycast()` |

---

## 14. 版本历史 (Version History)

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 2.2.0 | 2026-03-03 | **路径规划增强**：新增途径点事件（PATH_WAYPOINT_ADDED/REMOVED/CLEARED）、覆盖模式事件（PATH_COVERAGE_MODE_CHANGED/PROGRESS/COMPLETED）、避障配置事件（PATH_OBSTACLE_AVOIDANCE_CHANGED）；定义 PathPlanningConfig 数据结构和交互流程 |
| 2.1.0 | 2026-03-03 | **交互协议**：新增交互协议章节，定义鼠标交互规范、坐标系与旋转方向、视觉反馈、交互事件；解决相机与实体同时操作问题 |
| 2.0.1 | 2026-03-02 | **路径规划增强**：新增路径选择事件（PATH_START_SELECTED、PATH_END_SELECTED、PATH_SELECTION_MODE_CHANGED、PATH_SELECTION_CLEARED），支持多视图同步选择起点/终点 |
| 2.0.0 | 2026-03-02 | **重大重构**：协议重新定位为虚拟世界通用协议；ElementType 简化为 SPACE/ENTITY；业务分类通过 category 实现；移除所有领域特定事件 |
| 1.5.0 | 2026-03-02 | 模型库支持：新增模型库事件、元素模板管理、智能回退渲染机制 |
| 1.4.0 | 2026-03-02 | 机器人支持：新增机器人事件、元素管理混入类，支持机器人位置同步 |
| 1.3.0 | 2026-03-02 | 路径规划：新增路径规划事件、导航地图事件，集成 A* 算法 |
| 1.2.0 | 2026-03-02 | 功能扩展：添加场景边界、布局居中事件、编辑模式事件 |
| 1.1.0 | 2026-03-02 | 重大更新：添加统一元素模型、统一元素事件、元素注册表 |
| 1.0.0 | 2026-02-28 | 初始版本：发布-订阅模式、位置优先、坐标系统规范 |

---

## 15. 未来规划 (Roadmap)

### 15.1 v2.2.0 计划

- [ ] **分布式支持**：跨进程、跨设备同步
- [ ] **冲突解决**：CRDT 集成，支持多人协作

### 15.2 v2.3.0 计划

- [ ] **事件溯源**：时间旅行、状态回滚
- [ ] **跨语言 SDK**：JavaScript/TypeScript 支持

### 15.3 v3.0.0 愿景

- [ ] **标准化**：提交为开放标准
- [ ] **生态建设**：支持 Three.js、Unity、Unreal Engine

---

## 附录 A：迁移指南 (Migration Guide)

### 从 v1.x 迁移到 v2.0

#### ElementType 变更

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

#### 事件类型变更

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

#### 代码迁移示例

```python
# v1.x
view_sync.publish_room_position_changed("room_001", 2.0, 3.0, 0)

# v2.0
view_sync.publish_element_position_changed("room_001", ElementType.SPACE, 2.0, 3.0, 0)
```

```python
# v1.x
view_sync.publish_device_state_changed("device_001", DeviceState.ON)

# v2.0
element = SceneElement.create_entity(
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

# v2.0 订阅（统一处理）
view_sync.subscribe(ViewSyncEvents.ELEMENT_POSITION_CHANGED, on_position_changed)

def on_position_changed(event):
    target_type = event.target_type
    category = event.extra.get("category", "")
    # 根据 target_type 和 category 分别处理
```
