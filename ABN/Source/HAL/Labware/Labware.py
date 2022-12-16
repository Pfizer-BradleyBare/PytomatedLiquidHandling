from ...Tools.AbstractClasses import ObjectABC
from .Dimensions.LabwareDimensions import LabwareDimensions
from .Wells.Wells import Wells


class Labware(ObjectABC):
    def __init__(
        self,
        Name: str,
        Filter: str | None,
        LabwareWells: Wells | None,
        Dimensions: LabwareDimensions,
    ):
        self.Name: str = Name
        self.Filter: str | None = Filter
        self.Dimensions: LabwareDimensions = Dimensions
        self.LabwareWells: Wells | None = LabwareWells

    def GetName(self) -> str:
        return self.Name
