from .....Tools.AbstractClasses import ObjectABC


class LoadOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        CarrierTrackStart: int,
        CarrierTrackEnd: int,
        LabwareName: str,
        LabwareCarrierPositions: str,
        LabwarePartNumber: str,
    ):

        self.Name: str = Name

        self.CarrierTrackStart: str = str(CarrierTrackStart)
        self.CarrierTrackEnd: str = str(CarrierTrackEnd)

        self.LabwareName: str = LabwareName
        self.LabwareCarrierPositions: str = LabwareCarrierPositions
        self.LabwarePartNumber: str = LabwarePartNumber

        self.ShowExtendedInstructions: bool = False

    def GetName(self) -> str:
        return self.Name
