from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.Dimensions import Dimensions


class Labware(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Filters: list[str],
        DimensionsInstance: Dimensions,
    ):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.Filters: list[str] = Filters
        self.DimensionsInstance: Dimensions = DimensionsInstance

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
