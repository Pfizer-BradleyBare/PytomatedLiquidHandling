from . import Base
from .CoverableItem import CoverableItem
from .Lid import Lid
from .NonCoverableItem import NonCoverableItem

__Objects: dict[str, Base.LayoutItemABC] = dict()


def GetObjects() -> dict[str, Base.LayoutItemABC]:
    return __Objects
