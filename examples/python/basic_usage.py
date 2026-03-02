"""
LSH Protocol Example: Basic Usage

This example demonstrates the basic usage of the LSH protocol.
"""

from lsh import (
    SceneElement,
    ElementType,
    view_sync,
    ViewSyncEvents,
    SceneElementRegistry,
)


def on_element_added(event):
    """Handle element added event"""
    category = event.extra.get("category", "")
    print(f"[EVENT] Element added: {event.extra['name']} (category={category})")


def on_position_changed(event):
    """Handle position changed event"""
    pos = event.position
    print(f"[EVENT] Position changed: {event.target_id} -> ({pos.x}, {pos.y}, {pos.z})")


def main():
    print("=" * 50)
    print("LSH Protocol v2.0.0 - Basic Usage Example")
    print("=" * 50)
    
    # Subscribe to events
    view_sync.subscribe(ViewSyncEvents.ELEMENT_ADDED, on_element_added)
    view_sync.subscribe(ViewSyncEvents.ELEMENT_POSITION_CHANGED, on_position_changed)
    
    # Create a registry
    registry = SceneElementRegistry()
    
    # Create a space (room)
    print("\n1. Creating a space (room)...")
    room = SceneElement.create_space(
        id="room_001",
        name="Living Room",
        position=(0, 0, 0),
        size=(5.0, 4.0, 2.8),
        category="room"
    )
    registry.register(room)
    view_sync.publish_element_added(room)
    
    # Create entities (devices)
    print("\n2. Creating entities (devices)...")
    light = SceneElement.create_entity(
        id="device_001",
        name="Smart Light",
        position=(2.5, 2.0, 1.5),
        category="device",
        parent_id="room_001",
        extra={"state": "off"}
    )
    registry.register(light)
    view_sync.publish_element_added(light)
    
    sensor = SceneElement.create_entity(
        id="device_002",
        name="Temperature Sensor",
        position=(1.0, 1.0, 1.0),
        category="device",
        parent_id="room_001",
        extra={"temperature": 25.0}
    )
    registry.register(sensor)
    view_sync.publish_element_added(sensor)
    
    # Move an entity
    print("\n3. Moving an entity...")
    view_sync.publish_element_position_changed(
        "device_001", ElementType.ENTITY, 3.0, 2.5, 1.5
    )
    
    # Search elements
    print("\n4. Searching elements...")
    results = registry.search("light", categories=["device"])
    print(f"   Found: {[e.name for e in results]}")
    
    # Get by category
    print("\n5. Getting elements by category...")
    devices = registry.get_by_category("device")
    print(f"   Devices: {[e.name for e in devices]}")
    
    # Get children
    print("\n6. Getting children of room_001...")
    children = registry.get_children("room_001")
    print(f"   Children: {[e.name for e in children]}")
    
    # Statistics
    print("\n7. Registry statistics...")
    print(f"   Total elements: {registry.count()}")
    print(f"   By type: {registry.count_by_type()}")
    print(f"   By category: {registry.count_by_category()}")
    
    print("\n" + "=" * 50)
    print("Example completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
