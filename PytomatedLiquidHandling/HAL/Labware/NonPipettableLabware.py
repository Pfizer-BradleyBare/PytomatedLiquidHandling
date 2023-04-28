from .BaseLabware import Labware, LabwareDimensions, Wells


class NonPipettableLabware(Labware):
    def __init__(
        self,
        Name: str,
        Filters: list[str],
        Dimensions: LabwareDimensions,
    ):
        Labware.__init__(self, Name, Filters, Dimensions)
