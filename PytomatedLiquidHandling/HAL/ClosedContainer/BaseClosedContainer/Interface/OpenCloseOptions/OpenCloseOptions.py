from ......Driver.Tools.AbstractOptions import AdvancedMultiOptionsABC
from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....LayoutItem import CoverablePosition, NonCoverablePosition


class OpenCloseOptions(NonUniqueObjectABC):
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
