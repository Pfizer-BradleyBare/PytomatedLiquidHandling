from ...Tools.AbstractClasses import ObjectABC
from ..Transport.BaseTransportDevice import TransportDeviceTracker


class LoadingConfig:
    def __init__(self, CarrierLabwareString: str, CarrierPosition: int):
        self.CarrierLabwareString: str = CarrierLabwareString
        self.CarrierPosition: int = CarrierPosition

    def GetCarrierLabwareString(self) -> str:
        return self.CarrierLabwareString

    def GetCarrierPosition(self) -> int:
        return self.CarrierPosition


class DeckLocation(ObjectABC):
    def __init__(
        self,
        Name: str,
        SupportedTransportDeviceTrackerInstance: TransportDeviceTracker,
        LoadingConfigInstance: LoadingConfig | None,
        IsStorageLocation: bool,
    ):
        self.Name: str = Name
        self.SupportedTransportDeviceTrackerInstance: TransportDeviceTracker = (
            SupportedTransportDeviceTrackerInstance
        )
        self.LoadingConfigInstance: LoadingConfig | None = LoadingConfigInstance
        self.StorageLocation: bool = IsStorageLocation

    def GetName(self) -> str:
        return self.Name

    def IsStorageLocation(self) -> bool:
        return self.StorageLocation

    def IsLoadableLocation(self) -> bool:
        return self.LoadingConfigInstance is not None

    def GetLoadingConfig(self) -> LoadingConfig:
        if self.LoadingConfigInstance is None:
            raise Exception(
                "This is not a loadable location. Did you check if it is a IsLoadableLocation first?"
            )
        return self.LoadingConfigInstance
