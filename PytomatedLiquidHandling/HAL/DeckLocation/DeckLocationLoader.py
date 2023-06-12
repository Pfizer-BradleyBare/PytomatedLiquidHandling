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

        TransportDeviceInstance = TransportDeviceTrackerInstance.GetObjectByName(
            TransportDeviceID
        )

        TransportDeviceConfigInstance = TransportDeviceConfig(
            TransportDeviceInstance.UniqueIdentifier,
            HomeGetConfig,
            HomePlaceConfig,
            AwayGetConfig,
            AwayPlaceConfig,
        )

        if not all(
            Key in TransportDeviceConfigInstance.HomeGetConfig
            for Key in TransportDeviceInstance.GetGetConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Home Get Config. Please fix. Expected: "
                + str(TransportDeviceInstance.GetGetConfigKeys())
            )

        if not all(
            Key in TransportDeviceConfigInstance.HomePlaceConfig
            for Key in TransportDeviceInstance.GetPlaceConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Home Place Config. Please fix. Expected: "
                + str(TransportDeviceInstance.GetPlaceConfigKeys())
            )

        if not all(
            Key in TransportDeviceConfigInstance.AwayGetConfig
            for Key in TransportDeviceInstance.GetGetConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Away Get Config. Please fix. Expected: "
                + str(TransportDeviceInstance.GetGetConfigKeys())
            )

        if not all(
            Key in TransportDeviceConfigInstance.AwayPlaceConfig
            for Key in TransportDeviceInstance.GetPlaceConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Away Place Config. Please fix. Expected: "
                + str(TransportDeviceInstance.GetPlaceConfigKeys())
            )
        # Confirm expected keys are in ExtraConfig

        DeckLocationInstance = DeckLocation(
            UniqueIdentifier, TransportDeviceConfigInstance
        )

        DeckLocationTrackerInstance.LoadSingle(DeckLocationInstance)

    return DeckLocationTrackerInstance
