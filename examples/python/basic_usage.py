"""
LSH Protocol Example: Basic Usage

LSH 协议示例：基本用法

演示 LSH 协议的核心功能：
- 万物皆元素
- 属性驱动
- 无限扩展
"""

from lsh import (
    SceneElement,
    SceneElementRegistry,
    view_sync,
    ViewSyncEvents,
)


def on_element_added(event):
    """处理元素添加事件"""
    name = event.properties.get("name", "")
    category = event.properties.get("category", "")
    print(f"[EVENT] 元素添加: {name} (category={category})")


def main():
    print("=" * 50)
    print("LSH 协议 v3.2 - 万物皆元素，属性驱动")
    print("=" * 50)
    
    view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
    
    registry = SceneElementRegistry()
    
    print("\n1. 创建空白元素...")
    empty = SceneElement.create()
    print(f"   空白元素 ID: {empty.id}")
    
    print("\n2. 创建房间...")
    room = SceneElement.create({
        "name": "客厅",
        "category": "room",
        "position": [0, 0, 0],
        "size": [5.0, 4.0, 2.8],
        "room_type": "living_room"
    })
    registry.register(room)
    view_sync.publish_element_added(room)
    
    print("\n3. 创建设备...")
    light = SceneElement.create({
        "name": "智能灯",
        "category": "device",
        "position": [2.5, 2.0, 1.5],
        "device_type": "light",
        "state": "off",
        "parent_id": room.id
    })
    registry.register(light)
    view_sync.publish_element_added(light)
    
    print("\n4. 创建家具...")
    sofa = SceneElement.create({
        "name": "沙发",
        "category": "furniture",
        "position": [4, 3, 0],
        "size": [2.5, 1, 0.8],
        "eng_name": "sofa",
        "color": "#8B4513"
    })
    registry.register(sofa)
    view_sync.publish_element_added(sofa)
    
    print("\n5. 创建抽象元素（磁场）...")
    field = SceneElement.create({"name": "磁场"})
    registry.register(field)
    print(f"   磁场 ID: {field.id}")
    
    print("\n6. 属性操作...")
    print(f"   沙发名称: {sofa.get_property('name')}")
    print(f"   沙发颜色: {sofa.get_property('color')}")
    sofa.set_property("color", "red")
    print(f"   沙发新颜色: {sofa.get_property('color')}")
    
    print("\n7. 按属性查找...")
    devices = registry.find_by_property("category", "device")
    print(f"   设备: {[e.get_property('name') for e in devices]}")
    
    sofas = registry.find_by_property("name", "沙发")
    print(f"   沙发: {[e.get_property('name') for e in sofas]}")
    
    print("\n8. 搜索...")
    results = registry.search("灯")
    print(f"   搜索'灯': {[e.get_property('name') for e in results]}")
    
    print("\n9. 统计...")
    print(f"   元素总数: {registry.count()}")
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
