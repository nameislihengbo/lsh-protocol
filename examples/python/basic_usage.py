"""
LSH Protocol Example: Basic Usage

LSH 协议示例：基本用法 - 虚拟现实交互协议

演示 LSH 协议的核心功能：
- 万物皆元素
- 属性驱动
- 无限扩展
- 交互同步
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
    print("LSH 协议 v3.2 - 虚拟现实交互协议")
    print("万物皆元素，属性驱动，无限扩展")
    print("=" * 50)
    
    view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
    
    registry = SceneElementRegistry()
    
    print("\n1. 创建元素（万物皆元素）...")
    element = SceneElement.create({
        "name": "客厅",
        "category": "room",
        "position": [3, 3, 0],
        "size": [6, 6, 3]
    })
    registry.register(element)
    view_sync.publish_element_added(element)
    print(f"   元素 ID: {element.id}")
    print(f"   元素名称: {element.get_property('name')}")
    print(f"   元素分类: {element.get_property('category')}")
    
    print("\n2. 属性操作...")
    print(f"   获取名称: {element.get_property('name')}")
    element.set_property("room_type", "living_room")
    print(f"   设置房间类型: {element.get_property('room_type')}")
    
    print("\n3. 创建子元素...")
    parent_id = element.id
    element = SceneElement.create({
        "name": "客厅灯",
        "category": "device",
        "position": [3, 3, 2.8],
        "device_type": "light",
        "state": "off",
        "parent_id": parent_id
    })
    registry.register(element)
    view_sync.publish_element_added(element)
    
    print("\n4. 按属性查找...")
    rooms = registry.find_by_property("category", "room")
    print(f"   房间: {[e.get_property('name') for e in rooms]}")
    
    devices = registry.find_by_property("category", "device")
    print(f"   设备: {[e.get_property('name') for e in devices]}")
    
    print("\n5. 统计...")
    print(f"   元素总数: {registry.count()}")
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
