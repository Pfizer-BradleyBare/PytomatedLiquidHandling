from ....Tools.AbstractClasses import UniqueObjectABC
from .Dimensions.Dimensions import Dimensions


class LabwareABC(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        DimensionsInstance: Dimensions,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.DimensionsInstance: Dimensions = DimensionsInstance