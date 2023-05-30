from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        LayoutItemInstance: CoverablePosition | NonCoverablePosition,
        Position: int,
    ):
        self.LayoutItemInstance: CoverablePosition | NonCoverablePosition = (
            LayoutItemInstance
        )
        self.Position: int = Position
