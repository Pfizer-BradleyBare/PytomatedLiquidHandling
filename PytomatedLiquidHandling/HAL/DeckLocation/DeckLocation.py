from ...Tools.AbstractClasses import UniqueObjectABC
from .DeckLoadingConfig.DeckLoadingConfig import DeckLoadingConfig
from .LocationTransportDevice.LocationTransportDeviceTracker import (
    LocationTransportDeviceTracker,
)


class DeckLocation(UniqueObjectABC):
    def __init__(
        self,
        Name: str,
        SupportedLocationTransportDeviceTrackerInstance: LocationTransportDeviceTracker,
        DeckLoadingConfigInstance: DeckLoadingConfig | None,
        IsStorageLocation: bool,
        IsPipettableLocation: bool,
    ):
        self.Name: str = Name
        self.SupportedLocationTransportDeviceTrackerInstance: LocationTransportDeviceTracker = (
            SupportedLocationTransportDeviceTrackerInstance
        )
        self.DeckLoadingConfigInstance: DeckLoadingConfig | None = (
            DeckLoadingConfigInstance
        )
        self.StorageLocation: bool = IsStorageLocation
        self.PipettableLocation: bool = IsPipettableLocation

    def GetName(self) -> str:
        return self.Name

    def IsStorageLocation(self) -> bool:
        return self.StorageLocation

    def IsPipettableLocation(self) -> bool:
        return self.PipettableLocation

    def IsLoadableLocation(self) -> bool:
        return self.DeckLoadingConfigInstance is not None

    def GetDeckLoadingConfig(self) -> DeckLoadingConfig:
        if self.DeckLoadingConfigInstance is None:
            raise Exception(
                "This is not a loadable location. Did you check if it is a IsLoadableLocation first?"
            )
        return self.DeckLoadingConfigInstance
