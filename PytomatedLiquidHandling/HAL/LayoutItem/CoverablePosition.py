from .BaseLayoutItem import LayoutItemABC
from .Lid import Lid
from dataclasses import dataclass


@dataclass
class CoverablePosition(LayoutItemABC):
    LidInstance: Lid
