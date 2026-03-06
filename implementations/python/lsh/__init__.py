"""
LSH Protocol - Python Implementation

Li Shi Hang View Synchronization Protocol
A protocol for virtual world view synchronization.
"""


from .core import (
    ElementType,
    HierarchyPolicy,
    Bounds,
    SceneElement,
    SceneElementRegistry,
)
from .sync import (
    ViewSyncEvents,
    PositionData,
    SizeData,
    ViewSyncEvent,
    ViewSyncManager,
    view_sync,
)

__version__ = "2.6.1"
__author__ = "Li Hengbo"
__license__ = "MIT"

__all__ = [
    # Core types
    "ElementType",
    "HierarchyPolicy",
    "Bounds",
    "SceneElement",
    "SceneElementRegistry",
    # Sync types
    "ViewSyncEvents",
    "PositionData",
    "SizeData",
    "ViewSyncEvent",
    "ViewSyncManager",
    "view_sync",
]
