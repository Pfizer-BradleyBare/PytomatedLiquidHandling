from .BaseLabware import Dimensions, LabwareABC


class NonPipettableLabware(LabwareABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        DimensionsInstance: Dimensions,
    ):
        LabwareABC.__init__(self, UniqueIdentifier, DimensionsInstance)
