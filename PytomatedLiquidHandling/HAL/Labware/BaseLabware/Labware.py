from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.Dimensions import Dimensions


class Labware(UniqueObjectABC):
    def __init__(
        self,
        Name: str,
        Filters: list[str],
        DimensionsInstance: Dimensions,
    ):
        self.Name: str = Name
        self.Filters: list[str] = Filters
        self.DimensionsInstance: Dimensions = DimensionsInstance

    def GetName(self) -> str:
        return self.Name
