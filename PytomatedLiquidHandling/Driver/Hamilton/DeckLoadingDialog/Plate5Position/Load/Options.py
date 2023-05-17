from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
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
