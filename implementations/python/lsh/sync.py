"""
LSH Protocol Synchronization Types

LSH 协议同步机制 - 虚拟现实交互协议
- ViewSyncEvents: 事件类型
- PositionData: 位置数据
- SizeData: 尺寸数据
- ViewSyncEvent: 事件数据
- ViewSyncManager: 同步管理器

设计哲学：
- 万物皆元素：所有对象都是元素
- 属性驱动：所有内容通过属性表达
- 无限扩展：任意属性，无限可能
- 交互同步：发布-订阅模式，交互实时同步到所有端
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass, field
import logging

if TYPE_CHECKING:
    from .core import SceneElement

logger = logging.getLogger(__name__)

LSH_PROTOCOL_VERSION = "3.2.0"


class ViewSyncEvents(Enum):
    """视图同步事件类型"""
    
    ELEMENT_ADDED = "element_added"
    ELEMENT_DELETED = "element_deleted"
    ELEMENT_CHANGED = "element_changed"
    ELEMENT_POSITION_CHANGED = "element_position_changed"
    ELEMENT_VISIBILITY_CHANGED = "element_visibility_changed"
    
    SCENE_ACTIVATED = "scene_activated"
    SCENE_CHANGED = "scene_changed"
    
    LAYOUT_LOADED = "layout_loaded"
    LAYOUT_CHANGED = "layout_changed"
    FULL_REFRESH = "full_refresh"


@dataclass
class PositionData:
    """位置数据"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PositionData':
        return cls(
            x=data.get("x", 0.0),
            y=data.get("y", 0.0),
            z=data.get("z", 0.0)
        )
    
    @classmethod
    def from_tuple(cls, t: tuple) -> 'PositionData':
        return cls(
            x=t[0] if len(t) > 0 else 0.0,
            y=t[1] if len(t) > 1 else 0.0,
            z=t[2] if len(t) > 2 else 0.0
        )


@dataclass
class SizeData:
    """尺寸数据"""
    width: float = 1.0
    depth: float = 1.0
    height: float = 1.0
    
    def to_dict(self) -> Dict[str, float]:
        return {"width": self.width, "depth": self.depth, "height": self.height}
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.width, self.depth, self.height)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SizeData':
        return cls(
            width=data.get("width", 1.0),
            depth=data.get("depth", 1.0),
            height=data.get("height", 1.0)
        )
    
    @classmethod
    def from_tuple(cls, t: tuple) -> 'SizeData':
        return cls(
            width=t[0] if len(t) > 0 else 1.0,
            depth=t[1] if len(t) > 1 else 1.0,
            height=t[2] if len(t) > 2 else 1.0
        )


@dataclass
class ViewSyncEvent:
    """视图同步事件数据"""
    event_type: ViewSyncEvents
    target_id: str
    position: Optional[PositionData] = None
    size: Optional[SizeData] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "event_type": self.event_type.value,
            "target_id": self.target_id,
        }
        if self.position:
            result["position"] = self.position.to_dict()
        if self.size:
            result["size"] = self.size.to_dict()
        if self.properties:
            result["properties"] = self.properties
        if self.source:
            result["source"] = self.source
        return result


class ViewSyncManager:
    """视图同步管理器
    
    使用发布-订阅模式管理视图同步。
    
    Usage:
        view_sync = ViewSyncManager.instance()
        
        view_sync.publish_element_added(element)
        view_sync.publish_element_position_changed(id, x, y, z)
        
        view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, callback)
    """
    
    _instance: Optional['ViewSyncManager'] = None
    
    def __init__(self):
        self._subscribers: Dict[ViewSyncEvents, List[Callable]] = {
            event: [] for event in ViewSyncEvents
        }
        self._enabled = True
    
    @classmethod
    def instance(cls) -> 'ViewSyncManager':
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def subscribe(self, event_type: ViewSyncEvents, 
                  callback: Callable[[ViewSyncEvent], None]):
        """订阅事件"""
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: ViewSyncEvents, callback: Callable):
        """取消订阅"""
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
    
    def publish(self, event: ViewSyncEvent):
        """发布事件"""
        if not self._enabled:
            return
        
        for callback in self._subscribers[event.event_type]:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"View sync callback failed: {e}")
    
    def enable(self):
        """启用同步"""
        self._enabled = True
    
    def disable(self):
        """禁用同步"""
        self._enabled = False
    
    def publish_element_added(self, element: 'SceneElement'):
        """发布元素添加事件"""
        position = element.get_property("position", [0, 0, 0])
        size = element.get_property("size", [1, 1, 1])
        
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_ADDED,
            target_id=element.id,
            position=PositionData.from_tuple(tuple(position)),
            size=SizeData.from_tuple(tuple(size)),
            properties=element.properties.copy()
        ))
    
    def publish_element_deleted(self, element_id: str, properties: dict = None):
        """发布元素删除事件"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_DELETED,
            target_id=element_id,
            properties=properties or {}
        ))
    
    def publish_element_changed(self, element: 'SceneElement', changes: dict = None):
        """发布元素变更事件"""
        position = element.get_property("position", [0, 0, 0])
        size = element.get_property("size", [1, 1, 1])
        
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_CHANGED,
            target_id=element.id,
            position=PositionData.from_tuple(tuple(position)),
            size=SizeData.from_tuple(tuple(size)),
            properties={**element.properties.copy(), "changes": changes or []}
        ))
    
    def publish_element_position_changed(self, element_id: str,
                                          x: float, y: float, z: float = 0.0,
                                          source: str = None):
        """发布位置变更事件"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_POSITION_CHANGED,
            target_id=element_id,
            position=PositionData(x, y, z),
            source=source
        ))
    
    def publish_element_visibility_changed(self, element_id: str, visible: bool):
        """发布可见性变更事件"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_VISIBILITY_CHANGED,
            target_id=element_id,
            properties={"visible": visible}
        ))
    
    def publish_full_refresh(self):
        """发布全量刷新事件"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.FULL_REFRESH,
            target_id=""
        ))
    
    def publish_layout_loaded(self):
        """发布布局加载事件"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.LAYOUT_LOADED,
            target_id=""
        ))
    
    def publish_layout_changed(self):
        """发布布局变更事件"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.LAYOUT_CHANGED,
            target_id=""
        ))


view_sync = ViewSyncManager.instance()
