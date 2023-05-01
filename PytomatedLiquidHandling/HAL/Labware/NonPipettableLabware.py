from .BaseLabware import Dimensions, Labware


class NonPipettableLabware(Labware):
    def __init__(
        self,
        UniqueIdentifier: str,
        Filters: list[str],
        DimensionsInstance: Dimensions,
    ):
        Labware.__init__(self, UniqueIdentifier, Filters, DimensionsInstance)
