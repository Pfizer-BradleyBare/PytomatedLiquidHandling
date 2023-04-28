from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.LabwareDimensions import LabwareDimensions


class Labware(UniqueObjectABC):
    def __init__(
        self,
        Name: str,
        Filters: list[str],
        LabwareDimensionsInstance: LabwareDimensions,
    ):
        self.Name: str = Name
        self.Filters: list[str] = Filters
        self.LabwareDimensionsInstance: LabwareDimensions = LabwareDimensionsInstance

    def GetName(self) -> str:
        return self.Name
