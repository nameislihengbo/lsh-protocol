"""
LSH Protocol - Python Implementation

Li Shi Hang Protocol v3.0
A virtual-reality bridging protocol for unified element modeling.

Design Philosophy:
- LSH is a virtual-reality bridging protocol
- 万物皆元素: Everything (virtual/real) is an element
- 万物皆可包含: Everything can contain children
- Differences expressed through properties (category, extra)
"""


from .core import (
    HierarchyPolicy,
    Bounds,
    CATEGORY_DEFAULTS,
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
    LSH_PROTOCOL_VERSION,
)

__version__ = "3.0.1"
__author__ = "Li Hengbo"
__license__ = "MIT"

__all__ = [
    "HierarchyPolicy",
    "Bounds",
    "CATEGORY_DEFAULTS",
    "SceneElement",
    "SceneElementRegistry",
    "ViewSyncEvents",
    "PositionData",
    "SizeData",
    "ViewSyncEvent",
    "ViewSyncManager",
    "view_sync",
    "LSH_PROTOCOL_VERSION",
]
