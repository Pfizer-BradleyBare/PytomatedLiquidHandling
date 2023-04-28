from .BaseLabware import Dimensions, Labware


class NonPipettableLabware(Labware):
    def __init__(
        self,
        Name: str,
        Filters: list[str],
        DimensionsInstance: Dimensions,
    ):
        Labware.__init__(self, Name, Filters, DimensionsInstance)
