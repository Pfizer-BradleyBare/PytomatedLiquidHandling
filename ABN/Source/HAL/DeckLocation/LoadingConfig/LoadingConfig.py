class LoadingConfig:
    def __init__(self, CarrierLabwareString: str, CarrierPosition: int):
        self.CarrierLabwareString: str = CarrierLabwareString
        self.CarrierPosition: int = CarrierPosition

    def GetCarrierLabwareString(self) -> str:
        return self.CarrierLabwareString

    def GetCarrierPosition(self) -> int:
        return self.CarrierPosition
