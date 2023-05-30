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
        HomeConfig = Location["Transport Device"]["Home Config"]
        AwayConfig = Location["Transport Device"]["Away Config"]

        TransportDeviceConfigInstance = TransportDeviceConfig(
            TransportDeviceTrackerInstance.GetObjectByName(TransportDeviceID),
            HomeConfig,
            AwayConfig,
        )

        DeckLocationInstance = DeckLocation(
            UniqueIdentifier, TransportDeviceConfigInstance
        )

        DeckLocationTrackerInstance.LoadSingle(DeckLocationInstance)

    return DeckLocationTrackerInstance
