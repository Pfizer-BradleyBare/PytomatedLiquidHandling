from __future__ import annotations

from .layout_item_base import LayoutItemBase

__all__ = ["LayoutItemBase"]

identifier = str
devices: dict[identifier, LayoutItemBase] = {}
