from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from plh.hal import LayoutItem

if TYPE_CHECKING:
    from ..Orchastrator import Orchastrator


@dataclass
class Storage:
    OrchastratorInstance: Orchastrator

    StoredItems: LayoutItem.LayoutItemTracker = field(
        init=False,
        default_factory=LayoutItem.LayoutItemTracker,
    )

    def IsStored(self):
        ...

    def Acquire(self):
        ...

    def Release(self):
        ...
