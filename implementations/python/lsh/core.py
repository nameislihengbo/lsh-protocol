"""
LSH Protocol Core Types

LSH 协议核心类型

设计哲学：
- 万物皆元素：一切对象都是元素
- 属性驱动：所有内容都通过属性表达
- 无限扩展：任意属性，无限可能

三要素：
- 元素：一个空白容器
- 关系：ID（系统生成，用于标识）
- 属性：所有内容（name, category, position, size 等）
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


@dataclass
class SceneElement:
    """
    LSH 协议核心元素 - 万物皆元素
    
    一个空白元素容器，所有内容都通过属性注入。
    
    常用属性（示例）：
    - id: 唯一标识（系统生成）
    - name: 名称（如"沙发"）
    - category: 分类（device, furniture, room 等）
    - position: 位置 [x, y, z]
    - size: 尺寸 [width, depth, height]
    - eng_name: 英文名（如"sofa"）
    - 任意自定义属性...
    
    Examples:
        # 创建空白元素
        element = SceneElement.create()
        
        # 创建沙发
        sofa = SceneElement.create({
            "name": "沙发",
            "category": "furniture",
            "position": [4, 3, 0],
            "size": [2.5, 1, 0.8]
        })
        
        # 属性操作
        sofa.get_property("name")           # "沙发"
        sofa.set_property("color", "red")   # 设置颜色
        sofa.set_property("eng_name", "sofa")  # 扩展英文名
    """
    properties: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def id(self) -> str:
        """元素ID（从属性获取，如不存在则生成）"""
        if "id" not in self.properties:
            self.properties["id"] = f"elem_{uuid.uuid4().hex[:12]}"
        return self.properties["id"]
    
    @property
    def name(self) -> str:
        """元素名称（从属性获取）"""
        return self.properties.get("name", "")
    
    @name.setter
    def name(self, value: str):
        self.properties["name"] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """获取属性"""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> 'SceneElement':
        """设置属性（支持链式调用）"""
        self.properties[key] = value
        self.properties["updated_at"] = datetime.now().isoformat()
        return self
    
    def set_properties(self, properties: Dict[str, Any]) -> 'SceneElement':
        """批量设置属性"""
        self.properties.update(properties)
        self.properties["updated_at"] = datetime.now().isoformat()
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {"properties": self.properties.copy()}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneElement':
        """从字典创建"""
        return cls(properties=data.get("properties", {}))
    
    @classmethod
    def create(cls, properties: Dict[str, Any] = None) -> 'SceneElement':
        """创建元素
        
        创建一个空白元素，所有内容通过属性注入。
        ID 由系统自动生成，其他属性由用户定义。
        
        Args:
            properties: 属性字典，可包含任意属性：
                - name: 名称（如"沙发"）
                - category: 分类（device, furniture, room 等）
                - position: 位置 [x, y, z]
                - size: 尺寸 [width, depth, height]
                - 任意自定义属性...
                
        Returns:
            SceneElement 实例
            
        Examples:
            # 空白元素
            element = SceneElement.create()
            
            # 沙发
            sofa = SceneElement.create({
                "name": "沙发",
                "category": "furniture",
                "position": [4, 3, 0],
                "size": [2.5, 1, 0.8],
                "color": "#8B4513"
            })
            
            # 设备
            light = SceneElement.create({
                "name": "客厅灯",
                "category": "device",
                "position": [3, 3, 2.8],
                "state": "off"
            })
            
            # 磁场（抽象元素）
            field = SceneElement.create({"name": "磁场"})
        """
        props = (properties or {}).copy()
        if "id" not in props:
            props["id"] = f"elem_{uuid.uuid4().hex[:12]}"
        if "created_at" not in props:
            props["created_at"] = datetime.now().isoformat()
        props["updated_at"] = datetime.now().isoformat()
        return cls(properties=props)


class SceneElementRegistry:
    """
    元素注册表
    
    管理所有元素：
    - 注册/注销
    - 按属性查找
    - 搜索
    """
    
    def __init__(self):
        self._elements: Dict[str, SceneElement] = {}
    
    def register(self, element: SceneElement):
        """注册元素"""
        self._elements[element.id] = element
    
    def unregister(self, element_id: str) -> Optional[SceneElement]:
        """注销元素"""
        return self._elements.pop(element_id, None)
    
    def get(self, element_id: str) -> Optional[SceneElement]:
        """按ID获取元素"""
        return self._elements.get(element_id)
    
    def get_all(self) -> List[SceneElement]:
        """获取所有元素"""
        return list(self._elements.values())
    
    def find_by_property(self, key: str, value: Any) -> List[SceneElement]:
        """按属性查找元素
        
        Examples:
            # 查找所有设备
            registry.find_by_property("category", "device")
            
            # 查找名称为"沙发"的元素
            registry.find_by_property("name", "沙发")
            
            # 查找状态为开的所有元素
            registry.find_by_property("state", "on")
        """
        return [e for e in self._elements.values()
                if e.properties.get(key) == value]
    
    def find_one(self, key: str, value: Any) -> Optional[SceneElement]:
        """按属性查找单个元素"""
        for element in self._elements.values():
            if element.properties.get(key) == value:
                return element
        return None
    
    def search(self, query: str) -> List[SceneElement]:
        """搜索元素（在 name 和所有字符串属性中搜索）"""
        query_lower = query.lower()
        results = []
        for element in self._elements.values():
            # 搜索 name
            name = element.properties.get("name", "")
            if query_lower in name.lower():
                results.append(element)
                continue
            # 搜索所有字符串属性
            for v in element.properties.values():
                if isinstance(v, str) and query_lower in v.lower():
                    results.append(element)
                    break
        return results
    
    def delete(self, element_id: str) -> Optional[SceneElement]:
        """删除元素"""
        return self.unregister(element_id)
    
    def clear(self):
        """清空所有元素"""
        self._elements.clear()
    
    def count(self) -> int:
        """元素总数"""
        return len(self._elements)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {"elements": {eid: e.to_dict() for eid, e in self._elements.items()}}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneElementRegistry':
        """从字典创建"""
        registry = cls()
        for element_data in data.get("elements", {}).values():
            element = SceneElement.from_dict(element_data)
            registry.register(element)
        return registry
