from dataclasses import dataclass

from .BaseLayoutItem import LayoutItemABC


@dataclass
class NonCoverableItem(LayoutItemABC):
    ...
