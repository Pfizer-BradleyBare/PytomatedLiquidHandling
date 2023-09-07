from dataclasses import dataclass

from .Base import LayoutItemABC


@dataclass
class NonCoverableItem(LayoutItemABC):
    ...
