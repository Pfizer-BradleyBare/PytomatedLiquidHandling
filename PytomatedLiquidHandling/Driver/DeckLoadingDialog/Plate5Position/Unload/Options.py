from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        CarrierTrackStart: int,
        CarrierTrackEnd: int,
        LabwareName: str,
        LabwareCarrierPositions: str,
        LabwarePartNumber: str,
    ):

        self.CarrierTrackStart: str = str(CarrierTrackStart)
        self.CarrierTrackEnd: str = str(CarrierTrackEnd)

        self.LabwareName: str = LabwareName
        self.LabwareCarrierPositions: str = LabwareCarrierPositions
        self.LabwarePartNumber: str = LabwarePartNumber

        self.ShowExtendedInstructions: bool = False
