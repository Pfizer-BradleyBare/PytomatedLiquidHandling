from enum import Enum


class CarrierTypes(Enum):
    FTRCarrier5Position = "FTRCarrier5Position"
    PlateCarrier5Position = "PlateCarrier5Position"


class DeckLoadingConfig:
    def __init__(
        self,
        CarrierLabwareString: str,
        CarrierTrackStart: int,
        CarrierTrackEnd: int,
        CarrierType: CarrierTypes,
        CarrierPositions: str,
    ):
        self.CarrierLabwareString: str = CarrierLabwareString
        self.CarrierTrackStart: int = CarrierTrackStart
        self.CarrierTrackEnd: int = CarrierTrackEnd
        self.CarrierType: CarrierTypes = CarrierType
        self.CarrierPositions: str = CarrierPositions
