import yaml

from ..DeckLocation import DeckLoadingConfig, DeckLocationTracker, DeckLocation
from .BaseDeckLocation import TransportDeviceConfig
from ..TransportDevice.BaseTransportDevice import TransportDeviceTracker


def LoadYaml(
    TransportDeviceTrackerInstance: TransportDeviceTracker, FilePath: str
) -> DeckLocationTracker:
    DeckLocationTrackerInstance = DeckLocationTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Location in ConfigFile:
        if Location["Enabled"] == False:
            continue

        UniqueIdentifier = Location["Unique Identifier"]

        TransportDeviceID = Location["Transport Device"]["Unique Identifier"]
        HomeGetConfig = Location["Transport Device"]["Home Config"]["Get"]
        HomePlaceConfig = Location["Transport Device"]["Home Config"]["Place"]
        AwayGetConfig = Location["Transport Device"]["Away Config"]["Get"]
        AwayPlaceConfig = Location["Transport Device"]["Away Config"]["Place"]

        TransportDeviceConfigInstance = TransportDeviceConfig(
            TransportDeviceTrackerInstance.GetObjectByName(TransportDeviceID),
            HomeGetConfig,
            HomePlaceConfig,
            AwayGetConfig,
            AwayPlaceConfig,
        )

        DeckLocationInstance = DeckLocation(
            UniqueIdentifier, TransportDeviceConfigInstance
        )

        DeckLocationTrackerInstance.LoadSingle(DeckLocationInstance)

    return DeckLocationTrackerInstance
