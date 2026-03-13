"""
LSH Protocol Synchronization Types

Defines the synchronization mechanism for the LSH protocol:
- ViewSyncEvents: Event types
- PositionData: Position data structure
- SizeData: Size data structure
- ViewSyncEvent: Event data structure
- ViewSyncManager: Synchronization manager

LSH Protocol v3.0 - 虚拟与现实对接
- LSH is a virtual-reality bridging protocol
- 万物皆元素: Everything (virtual/real) is an element
- Removed ElementType distinction
- All elements use category for classification
- target_type now stores category string
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass, field
import logging

if TYPE_CHECKING:
    from .core import SceneElement

logger = logging.getLogger(__name__)

LSH_PROTOCOL_VERSION = "3.0.1"


class ViewSyncEvents(Enum):
    """View synchronization event types
    
    LSH Protocol v3.0 - 虚拟与现实对接
    
    Design principles:
    1. 万物皆元素: All elements (virtual/real) use ELEMENT_* events
    2. Distinguished by category: room/device/furniture/robot...
    3. Hierarchy: Managed through parent_id/children_ids
    4. Cascade updates: Children auto-update when parent moves
    """
    
    ELEMENT_ADDED = "element_added"
    ELEMENT_DELETED = "element_deleted"
    ELEMENT_CHANGED = "element_changed"
    ELEMENT_POSITION_CHANGED = "element_position_changed"
    ELEMENT_VISIBILITY_CHANGED = "element_visibility_changed"
    ELEMENT_HIERARCHY_CHANGED = "element_hierarchy_changed"
    ELEMENT_ROOM_CHANGED = "element_room_changed"
    ELEMENTS_SYNC = "elements_sync"
    
    SCENE_ACTIVATED = "scene_activated"
    SCENE_CHANGED = "scene_changed"
    SCENE_BOUNDS_CHANGED = "scene_bounds_changed"
    
    EDIT_MODE_CHANGED = "edit_mode_changed"
    
    PATH_CALCULATED = "path_calculated"
    PATH_VISUALIZED = "path_visualized"
    PATH_EXECUTED = "path_executed"
    PATH_START_SELECTED = "path_start_selected"
    PATH_END_SELECTED = "path_end_selected"
    PATH_WAYPOINT_ADDED = "path_waypoint_added"
    PATH_SELECTION_MODE_CHANGED = "path_selection_mode_changed"
    PATH_SELECTION_CLEARED = "path_selection_cleared"
    PATH_COVERAGE_PROGRESS = "path_coverage_progress"
    PATH_COVERAGE_COMPLETED = "path_coverage_completed"
    NAVIGATION_MAP_UPDATED = "navigation_map_updated"
    
    LAYOUT_LOADED = "layout_loaded"
    LAYOUT_CHANGED = "layout_changed"
    LAYOUT_CENTERED = "layout_centered"
    FULL_REFRESH = "full_refresh"


@dataclass
class PositionData:
    """Position data structure
    
    Shared position information across all views, 
    core of view synchronization.
    """
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
    """Size data structure"""
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
    """View synchronization event data structure
    
    LSH Protocol v3.0 - target_type stores category string
    """
    event_type: ViewSyncEvents
    target_id: str
    target_type: str = ""
    position: Optional[PositionData] = None
    size: Optional[SizeData] = None
    parent_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "event_type": self.event_type.value,
            "target_id": self.target_id,
            "target_type": self.target_type,
        }
        if self.position:
            result["position"] = self.position.to_dict()
        if self.size:
            result["size"] = self.size.to_dict()
        if self.parent_id:
            result["parent_id"] = self.parent_id
        if self.extra:
            result["extra"] = self.extra
        if self.source:
            result["source"] = self.source
        return result


class ViewSyncManager:
    """View synchronization manager
    
    Manages synchronization across all views using publish-subscribe pattern.
    
    Usage:
        view_sync = ViewSyncManager.instance()
        
        view_sync.publish_element_added(element)
        view_sync.publish_element_position_changed(id, category, x, y, z)
        
        view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, callback)
    """
    
    _instance: Optional['ViewSyncManager'] = None
    
    def __init__(self):
        self._subscribers: Dict[ViewSyncEvents, List[Callable]] = {
            event: [] for event in ViewSyncEvents
        }
        self._enabled = True
        self._batch_mode = False
        self._pending_events: List[ViewSyncEvent] = []
    
    @classmethod
    def instance(cls) -> 'ViewSyncManager':
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def subscribe(self, event_type: ViewSyncEvents, 
                  callback: Callable[[ViewSyncEvent], None]):
        """Subscribe to an event
        
        Args:
            event_type: Event type
            callback: Callback function receiving ViewSyncEvent
        """
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
            logger.debug(f"View subscribed to event: {event_type.value}")
    
    def unsubscribe(self, event_type: ViewSyncEvents, callback: Callable):
        """Unsubscribe from an event"""
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
    
    def publish(self, event: ViewSyncEvent):
        """Publish an event
        
        Args:
            event: View sync event
        """
        if not self._enabled:
            return
        
        if self._batch_mode:
            self._pending_events.append(event)
            return
        
        logger.debug(f"Publishing view sync event: {event.event_type.value}, target={event.target_id}")
        
        for callback in self._subscribers[event.event_type]:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"View sync callback failed: {callback.__name__}, error: {e}")
    
    def batch_begin(self):
        """Start batch mode
        
        In batch mode, all events are cached until batch_end() is called.
        """
        self._batch_mode = True
        self._pending_events.clear()
    
    def batch_end(self):
        """End batch mode, process cached events"""
        self._batch_mode = False
        
        merged_events = self._merge_events(self._pending_events)
        
        for event in merged_events:
            self.publish(event)
        
        self._pending_events.clear()
    
    def _merge_events(self, events: List[ViewSyncEvent]) -> List[ViewSyncEvent]:
        """Merge duplicate events for the same target"""
        if not events:
            return []
        
        latest_by_target: Dict[str, ViewSyncEvent] = {}
        
        for event in events:
            key = f"{event.event_type.value}_{event.target_id}"
            latest_by_target[key] = event
        
        return list(latest_by_target.values())
    
    def enable(self):
        """Enable synchronization"""
        self._enabled = True
    
    def disable(self):
        """Disable synchronization (for batch scene updates)"""
        self._enabled = False
    
    def publish_element_added(self, element: 'SceneElement'):
        """Publish element added event
        
        Args:
            element: Scene element object
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_ADDED,
            target_id=element.id,
            target_type=element.category,
            position=PositionData.from_tuple(tuple(element.position) if isinstance(element.position, list) else element.position),
            size=SizeData.from_tuple(tuple(element.size) if isinstance(element.size, list) else element.size) if element.size else None,
            parent_id=element.parent_id,
            extra={
                "name": element.name,
                "category": element.category,
                "tags": element.tags,
                "visible": element.visible,
                "searchable": element.searchable,
                "bounds": element.bounds.to_dict() if element.bounds else None,
                **element.extra
            }
        ))
    
    def publish_element_deleted(self, element_id: str, category: str = "",
                                 extra: dict = None):
        """Publish element deleted event
        
        Args:
            element_id: Element ID
            category: Element category
            extra: Extra information
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_DELETED,
            target_id=element_id,
            target_type=category,
            extra=extra or {}
        ))
    
    def publish_element_changed(self, element: 'SceneElement', changes: dict = None):
        """Publish element changed event
        
        Args:
            element: Scene element object
            changes: List of changed fields
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_CHANGED,
            target_id=element.id,
            target_type=element.category,
            position=PositionData.from_tuple(tuple(element.position) if isinstance(element.position, list) else element.position),
            size=SizeData.from_tuple(tuple(element.size) if isinstance(element.size, list) else element.size) if element.size else None,
            parent_id=element.parent_id,
            extra={
                "name": element.name,
                "category": element.category,
                "tags": element.tags,
                "changes": changes or [],
                **element.extra
            }
        ))
    
    def publish_element_position_changed(self, element_id: str, category: str,
                                          x: float, y: float, z: float = 0.0, source: str = None):
        """Publish element position changed event
        
        Args:
            element_id: Element ID
            category: Element category
            x, y, z: New position
            source: Event source identifier (for loop prevention)
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_POSITION_CHANGED,
            target_id=element_id,
            target_type=category,
            position=PositionData(x, y, z),
            source=source
        ))
    
    def publish_element_visibility_changed(self, element_id: str, category: str,
                                            visible: bool):
        """Publish element visibility changed event
        
        Args:
            element_id: Element ID
            category: Element category
            visible: Visibility
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_VISIBILITY_CHANGED,
            target_id=element_id,
            target_type=category,
            extra={"visible": visible}
        ))
    
    def publish_element_hierarchy_changed(self, element_id: str, category: str,
                                           old_parent_id: str = None, new_parent_id: str = None):
        """Publish element hierarchy changed event
        
        Args:
            element_id: Element ID
            category: Element category
            old_parent_id: Old parent ID
            new_parent_id: New parent ID
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_HIERARCHY_CHANGED,
            target_id=element_id,
            target_type=category,
            parent_id=new_parent_id,
            extra={
                "old_parent_id": old_parent_id,
                "new_parent_id": new_parent_id
            }
        ))
    
    def publish_element_room_changed(self, element_id: str, category: str,
                                      old_room_id: str = None, new_room_id: str = None):
        """Publish element room changed event
        
        Args:
            element_id: Element ID
            category: Element category
            old_room_id: Old room ID
            new_room_id: New room ID
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENT_ROOM_CHANGED,
            target_id=element_id,
            target_type=category,
            extra={
                "old_room_id": old_room_id,
                "new_room_id": new_room_id
            }
        ))
    
    def publish_elements_sync(self, elements: List['SceneElement']):
        """Publish elements sync event (batch sync all elements)
        
        Args:
            elements: List of scene elements
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.ELEMENTS_SYNC,
            target_id="",
            target_type="registry",
            extra={
                "elements": [e.to_dict() for e in elements],
                "count": len(elements)
            }
        ))
    
    def publish_full_refresh(self):
        """Publish full refresh event"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.FULL_REFRESH,
            target_id="",
            target_type="scene"
        ))
    
    def publish_layout_loaded(self):
        """Publish layout loaded event"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.LAYOUT_LOADED,
            target_id="",
            target_type="layout"
        ))
    
    def publish_layout_changed(self):
        """Publish layout changed event"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.LAYOUT_CHANGED,
            target_id="",
            target_type="layout"
        ))
    
    def publish_layout_centered(self, offset_x: float, offset_y: float, offset_z: float):
        """Publish layout centered event
        
        Args:
            offset_x: X offset
            offset_y: Y offset
            offset_z: Z offset
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.LAYOUT_CENTERED,
            target_id="",
            target_type="layout",
            position=PositionData(offset_x, offset_y, offset_z)
        ))
    
    def publish_scene_bounds_changed(self, min_x: float, max_x: float,
                                      min_y: float, max_y: float,
                                      min_z: float, max_z: float):
        """Publish scene bounds changed event
        
        Args:
            min_x, max_x: X bounds
            min_y, max_y: Y bounds
            min_z, max_z: Z bounds
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.SCENE_BOUNDS_CHANGED,
            target_id="",
            target_type="scene",
            extra={
                "min_x": min_x, "max_x": max_x,
                "min_y": min_y, "max_y": max_y,
                "min_z": min_z, "max_z": max_z
            }
        ))
    
    def publish_edit_mode_changed(self, enabled: bool):
        """Publish edit mode changed event
        
        Args:
            enabled: Whether edit mode is enabled
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.EDIT_MODE_CHANGED,
            target_id="",
            target_type="layout",
            extra={"is_edit": enabled}
        ))
    
    def publish_scene_activated(self, scene_id: str):
        """Publish scene activated event"""
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.SCENE_ACTIVATED,
            target_id=scene_id,
            target_type="scene"
        ))
    
    def publish_path_calculated(self, path: List, distance: float,
                                 estimated_time: float, waypoints: List = None):
        """Publish path calculated event
        
        Args:
            path: Path coordinates [(x, y, z), ...]
            distance: Path distance (meters)
            estimated_time: Estimated time (seconds)
            waypoints: Navigation waypoints
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.PATH_CALCULATED,
            target_id="",
            target_type="path",
            extra={
                "path": path,
                "distance": distance,
                "estimated_time": estimated_time,
                "waypoints": waypoints or []
            }
        ))
    
    def publish_path_visualized(self, path: List, view_type: str = "both",
                                 color: str = "green", clear_previous: bool = True):
        """Publish path visualized event
        
        Args:
            path: Path coordinates
            view_type: View type (2d/3d/both)
            color: Path color
            clear_previous: Whether to clear previous paths
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.PATH_VISUALIZED,
            target_id="",
            target_type="path",
            extra={
                "path": path,
                "view_type": view_type,
                "color": color,
                "clear_previous": clear_previous
            }
        ))
    
    def publish_path_executed(self, path_id: str, success: bool,
                               message: str = ""):
        """Publish path executed event
        
        Args:
            path_id: Path ID
            success: Whether successful
            message: Execution message
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.PATH_EXECUTED,
            target_id=path_id,
            target_type="path",
            extra={
                "success": success,
                "message": message
            }
        ))
    
    def publish_path_selection_mode_changed(self, mode: str):
        """Publish path selection mode changed event
        
        Args:
            mode: Selection mode ("start", "end", "waypoint", or "" to clear)
        """
        self.publish(ViewSyncEvent(
            event_type=ViewSyncEvents.PATH_SELECTION_MODE_CHANGED,
            target_id="",
            target_type="path",
            extra={"mode": mode}
        ))


view_sync = ViewSyncManager.instance()
