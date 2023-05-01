from .BaseLabware import Dimensions, Labware


class NonPipettableLabware(Labware):
    def __init__(
        self,
        UniqueIdentifier: str,
        DimensionsInstance: Dimensions,
    ):
        Labware.__init__(self, UniqueIdentifier, DimensionsInstance)
