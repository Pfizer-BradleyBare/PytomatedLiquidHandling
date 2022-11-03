from ..Transport import TransportDevice
from ...Tools.AbstractClasses import ObjectABC


class LoadingConfig:
    def __init__(self, CarrierLabwareString: str, CarrierPosition: int):
        self.CarrierLabwareString: str = CarrierLabwareString
        self.CarrierPosition: int = CarrierPosition

    def GetCarrierLabwareString(self) -> str:
        return self.CarrierLabwareString

    def GetCarrierPosition(self) -> int:
        return self.CarrierPosition


class DeckLocation(ObjectABC):
    def __init__(self, Name: str, SupportedTransportInstances: list[TransportDevice]):
        self.Name: str = Name
        self.SupportedTransportInstances: list[
            TransportDevice
        ] = SupportedTransportInstances

    def GetName(self) -> str:
        return self.Name

    def GetTransportInstances(self) -> list[TransportDevice]:
        return self.SupportedTransportInstances


class LoadableDeckLocation(DeckLocation):
    def __init__(
        self,
        Name: str,
        SupportedTransportInstances: list[TransportDevice],
        LoadingConfigInstance: LoadingConfig,
    ):
        DeckLocation.__init__(self, Name, SupportedTransportInstances)
        self.LoadingConfigInstance: LoadingConfig = LoadingConfigInstance

    def GetLoadingConfig(self) -> LoadingConfig:
        return self.LoadingConfigInstance
