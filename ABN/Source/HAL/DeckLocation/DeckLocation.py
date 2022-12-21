from ...Tools.AbstractClasses import ObjectABC
from .LoadingConfig.LoadingConfig import LoadingConfig
from .LocationTransportDevice.LocationTransportDeviceTracker import (
    LocationTransportDeviceTracker,
)


class DeckLocation(ObjectABC):
    def __init__(
        self,
        Name: str,
        SupportedLocationTransportDeviceTrackerInstance: LocationTransportDeviceTracker,
        LoadingConfigInstance: LoadingConfig | None,
        IsStorageLocation: bool,
        IsPipettableLocation: bool,
    ):
        self.Name: str = Name
        self.SupportedLocationTransportDeviceTrackerInstance: LocationTransportDeviceTracker = (
            SupportedLocationTransportDeviceTrackerInstance
        )
        self.LoadingConfigInstance: LoadingConfig | None = LoadingConfigInstance
        self.StorageLocation: bool = IsStorageLocation
        self.PipettableLocation: bool = IsPipettableLocation

    def GetName(self) -> str:
        return self.Name

    def IsStorageLocation(self) -> bool:
        return self.StorageLocation

    def IsPipettableLocation(self) -> bool:
        return self.PipettableLocation

    def IsLoadableLocation(self) -> bool:
        return self.LoadingConfigInstance is not None

    def GetLoadingConfig(self) -> LoadingConfig:
        if self.LoadingConfigInstance is None:
            raise Exception(
                "This is not a loadable location. Did you check if it is a IsLoadableLocation first?"
            )
        return self.LoadingConfigInstance
