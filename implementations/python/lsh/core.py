"""
LSH Protocol Core Types

Defines the core data structures for the LSH protocol v3.0:
- Bounds: Spatial boundaries
- SceneElement: Unified element model (万物皆元素)
- SceneElementRegistry: Element management

Design Philosophy:
- LSH is a virtual-reality bridging protocol
- 万物皆元素: Everything (virtual/real) is an element
- 万物皆可包含: Everything can contain children
- Differences expressed through properties (category, extra)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from enum import Enum


class HierarchyPolicy(Enum):
    """Hierarchy policy for element movement"""
    FIXED = "fixed"
    FOLLOW_PARENT = "follow_parent"
    INDEPENDENT = "independent"


@dataclass
class Bounds:
    """Spatial boundaries
    
    Defines the range of a space, used for:
    1. Rendering optimization (frustum culling)
    2. Collision detection
    3. Navigation mesh generation
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
        """Check if a point is within the bounds"""
        return (
            self.min_x <= x <= self.max_x and
            self.min_y <= y <= self.max_y and
            self.min_z <= z <= self.max_z
        )
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "min_x": self.min_x, "max_x": self.max_x,
            "min_y": self.min_y, "max_y": self.max_y,
            "min_z": self.min_z, "max_z": self.max_z
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Bounds':
        return cls(
            min_x=data.get("min_x", 0.0), max_x=data.get("max_x", 1.0),
            min_y=data.get("min_y", 0.0), max_y=data.get("max_y", 1.0),
            min_z=data.get("min_z", 0.0), max_z=data.get("max_z", 1.0)
        )
    
    @classmethod
    def from_size(cls, width: float, depth: float, height: float,
                  offset: Tuple[float, float, float] = (0, 0, 0)) -> 'Bounds':
        """Create bounds from size"""
        return cls(
            min_x=offset[0], max_x=offset[0] + width,
            min_y=offset[1], max_y=offset[1] + depth,
            min_z=offset[2], max_z=offset[2] + height
        )


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


@dataclass
class SceneElement:
    """
    Unified element model - 万物皆元素
    
    All elements (virtual/real) use this model for:
    1. Unified search
    2. Cross-view highlighting
    3. LSH synchronization
    
    Design Philosophy:
    - LSH is a virtual-reality bridging protocol
    - 万物皆元素: Everything (virtual/real) is an element
    - 万物皆可包含: Everything can contain children
    - Differences expressed through properties (category, extra)
    """
    id: str
    name: str
    
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotation: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    scale: float = 1.0
    
    size: List[float] = field(default_factory=lambda: [1.0, 1.0, 1.0])
    bounds: Optional[Bounds] = None
    
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    hierarchy_policy: HierarchyPolicy = HierarchyPolicy.FOLLOW_PARENT
    
    local_position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    local_rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    
    template_id: Optional[str] = None
    
    category: str = ""
    tags: List[str] = field(default_factory=list)
    
    extra: Dict[str, Any] = field(default_factory=dict)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    visible: bool = True
    searchable: bool = True
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get property from element
        
        Priority:
        1. extra field
        2. CATEGORY_DEFAULTS[category]
        """
        if key in self.extra:
            return self.extra[key]
        
        category_defaults = CATEGORY_DEFAULTS.get(self.category, {})
        if key in category_defaults:
            return category_defaults[key]
        
        return default
    
    def is_space(self) -> bool:
        """Check if this is a space type (has spatial bounds)"""
        return self.get_property("is_space", False)
    
    def is_toggleable(self) -> bool:
        """Check if this element can be toggled"""
        return self.get_property("is_toggleable", False)
    
    def is_movable(self) -> bool:
        """Check if this element can move autonomously"""
        return self.get_property("is_movable", False)
    
    def is_custom_model(self) -> bool:
        """Check if this is a custom imported model"""
        return self.get_property("is_custom_model", False)
    
    def get_extra_property(self, key: str, default: Any = None) -> Any:
        """Get property from extra dict"""
        return self.extra.get(key, default)
    
    def set_extra_property(self, key: str, value: Any):
        """Set property in extra dict"""
        self.extra[key] = value
    
    def get_world_position(self) -> Tuple[float, float, float]:
        """Get world coordinates (considering parent)"""
        return tuple(self.position)
    
    def get_local_position(self) -> Tuple[float, float, float]:
        """Get local coordinates relative to parent"""
        if self.parent_id:
            return self.local_position
        return tuple(self.position)
    
    def set_local_position(self, local_pos: Tuple[float, float, float], 
                           parent_pos: Tuple[float, float, float] = None):
        """Set local coordinates and update world coordinates"""
        self.local_position = local_pos
        if parent_pos:
            self.position = [
                parent_pos[0] + local_pos[0],
                parent_pos[1] + local_pos[1],
                parent_pos[2] + local_pos[2]
            ]
    
    def update_from_parent(self, parent_position: Tuple[float, float, float],
                           parent_rotation: Tuple[float, float, float] = None):
        """Update world coordinates based on parent position"""
        if self.hierarchy_policy == HierarchyPolicy.FOLLOW_PARENT:
            self.position = [
                parent_position[0] + self.local_position[0],
                parent_position[1] + self.local_position[1],
                parent_position[2] + self.local_position[2]
            ]
    
    def add_child(self, child_id: str):
        """Add a child element"""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)
    
    def remove_child(self, child_id: str) -> bool:
        """Remove a child element"""
        if child_id in self.children_ids:
            self.children_ids.remove(child_id)
            return True
        return False
    
    def has_children(self) -> bool:
        """Check if has children"""
        return len(self.children_ids) > 0
    
    def is_child_of(self, parent_id: str) -> bool:
        """Check if is a child of the specified element"""
        return self.parent_id == parent_id
    
    def update_bounds_from_size(self):
        """Update bounds from size"""
        self.bounds = Bounds.from_size(
            self.size[0], self.size[1], self.size[2],
            offset=tuple(self.position)
        )
    
    def update_timestamp(self):
        """Update timestamp"""
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "rotation": self.rotation,
            "scale": self.scale,
            "size": self.size,
            "bounds": self.bounds.to_dict() if self.bounds else None,
            "parent_id": self.parent_id,
            "children_ids": self.children_ids,
            "hierarchy_policy": self.hierarchy_policy.value,
            "local_position": self.local_position,
            "local_rotation": self.local_rotation,
            "template_id": self.template_id,
            "category": self.category,
            "tags": self.tags,
            "extra": self.extra,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "visible": self.visible,
            "searchable": self.searchable
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneElement':
        """Create from dictionary"""
        bounds_data = data.get("bounds")
        bounds = Bounds.from_dict(bounds_data) if bounds_data else None
        
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            position=list(data.get("position", [0, 0, 0])),
            rotation=list(data.get("rotation", [0, 0, 0])),
            scale=data.get("scale", 1.0),
            size=list(data.get("size", [1, 1, 1])),
            bounds=bounds,
            parent_id=data.get("parent_id"),
            children_ids=data.get("children_ids", []),
            hierarchy_policy=HierarchyPolicy(data.get("hierarchy_policy", "follow_parent")),
            local_position=tuple(data.get("local_position", [0, 0, 0])),
            local_rotation=tuple(data.get("local_rotation", [0, 0, 0])),
            template_id=data.get("template_id"),
            category=data.get("category", ""),
            tags=data.get("tags", []),
            extra=data.get("extra", {}),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            visible=data.get("visible", True),
            searchable=data.get("searchable", True)
        )
    
    @classmethod
    def create(cls, id: str, name: str, category: str = "",
               position: Tuple[float, float, float] = (0, 0, 0),
               size: Tuple[float, float, float] = (1, 1, 1),
               **kwargs) -> 'SceneElement':
        """Create an element"""
        element = cls(
            id=id,
            name=name,
            position=list(position),
            size=list(size),
            category=category,
            **kwargs
        )
        element.update_bounds_from_size()
        return element


class SceneElementRegistry:
    """
    Scene element registry
    
    Manages all scene elements with support for:
    1. Register/unregister elements
    2. Search by category/tag
    3. Hierarchy management
    """
    
    def __init__(self):
        self._elements: Dict[str, SceneElement] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._by_parent: Dict[str, List[str]] = {}
        self._by_tag: Dict[str, List[str]] = {}
    
    def register(self, element: SceneElement):
        """Register an element"""
        self._elements[element.id] = element
        
        if element.category:
            if element.category not in self._by_category:
                self._by_category[element.category] = []
            self._by_category[element.category].append(element.id)
        
        for tag in element.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = []
            self._by_tag[tag].append(element.id)
        
        if element.parent_id:
            if element.parent_id not in self._by_parent:
                self._by_parent[element.parent_id] = []
            self._by_parent[element.parent_id].append(element.id)
            
            parent = self._elements.get(element.parent_id)
            if parent:
                parent.add_child(element.id)
    
    def unregister(self, element_id: str) -> Optional[SceneElement]:
        """Unregister an element (cascades to children)"""
        if element_id not in self._elements:
            return None
        
        element = self._elements.pop(element_id)
        
        if element.category and element.category in self._by_category:
            if element_id in self._by_category[element.category]:
                self._by_category[element.category].remove(element_id)
        
        for tag in element.tags:
            if tag in self._by_tag and element_id in self._by_tag[tag]:
                self._by_tag[tag].remove(element_id)
        
        if element.parent_id and element.parent_id in self._by_parent:
            if element_id in self._by_parent[element.parent_id]:
                self._by_parent[element.parent_id].remove(element_id)
            parent = self._elements.get(element.parent_id)
            if parent:
                parent.remove_child(element_id)
        
        for child_id in element.children_ids[:]:
            self.unregister(child_id)
        
        return element
    
    def get(self, element_id: str) -> Optional[SceneElement]:
        """Get an element by ID"""
        return self._elements.get(element_id)
    
    def get_all(self) -> List[SceneElement]:
        """Get all elements"""
        return list(self._elements.values())
    
    def get_by_category(self, category: str) -> List[SceneElement]:
        """Get elements by category"""
        if category not in self._by_category:
            return []
        return [self._elements[eid] for eid in self._by_category[category] 
                if eid in self._elements]
    
    def get_by_tag(self, tag: str) -> List[SceneElement]:
        """Get elements by tag"""
        if tag not in self._by_tag:
            return []
        return [self._elements[eid] for eid in self._by_tag[tag] 
                if eid in self._elements]
    
    def get_children(self, parent_id: str) -> List[SceneElement]:
        """Get children of an element"""
        if parent_id not in self._by_parent:
            return []
        return [self._elements[eid] for eid in self._by_parent[parent_id] 
                if eid in self._elements]
    
    def get_parent(self, element_id: str) -> Optional[SceneElement]:
        """Get parent of an element"""
        element = self._elements.get(element_id)
        if element and element.parent_id:
            return self._elements.get(element.parent_id)
        return None
    
    def update_position_cascade(self, element_id: str, 
                                 new_position: Tuple[float, float, float]):
        """Cascade update position when parent moves"""
        element = self._elements.get(element_id)
        if not element:
            return
        
        element.position = list(new_position)
        element.update_timestamp()
        
        children = self.get_children(element_id)
        for child in children:
            if child.hierarchy_policy == HierarchyPolicy.FOLLOW_PARENT:
                child.update_from_parent(new_position)
                child.update_timestamp()
                self.update_position_cascade(child.id, tuple(child.position))
    
    def search(self, query: str, categories: List[str] = None,
               tags: List[str] = None) -> List[SceneElement]:
        """
        Search elements
        
        Args:
            query: Search keyword
            categories: Limit search to these categories (optional)
            tags: Limit search to these tags (optional)
        
        Returns:
            Matching elements
        """
        query_lower = query.lower()
        results = []
        
        for element in self._elements.values():
            if not element.searchable or not element.visible:
                continue
            
            if categories and element.category not in categories:
                continue
            
            if tags and not any(tag in element.tags for tag in tags):
                continue
            
            if query_lower in element.name.lower():
                results.append(element)
                continue
            
            if query_lower in element.category.lower():
                results.append(element)
                continue
            
            for key, value in element.extra.items():
                if isinstance(value, str) and query_lower in value.lower():
                    results.append(element)
                    break
        
        return results
    
    def clear(self):
        """Clear all elements"""
        self._elements.clear()
        self._by_category.clear()
        self._by_parent.clear()
        self._by_tag.clear()
    
    def count(self) -> int:
        """Get total element count"""
        return len(self._elements)
    
    def count_by_category(self) -> Dict[str, int]:
        """Count elements by category"""
        return {c: len(ids) for c, ids in self._by_category.items()}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (for persistence)"""
        return {
            "elements": {eid: e.to_dict() for eid, e in self._elements.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneElementRegistry':
        """Create from dictionary"""
        registry = cls()
        for element_data in data.get("elements", {}).values():
            element = SceneElement.from_dict(element_data)
            registry.register(element)
        return registry
