import yaml

from ..DeckLocation import (
    DeckLoadingConfig,
    DeckLocationTracker,
    LoadableDeckLocation,
    NonLoadableDeckLocation,
)
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
        IsStorageLocation = Location["Is Storage Location"]
        IsPipettableLocation = Location["Is Pipettable Location"]

        if "Deck Location" in Location:
            CarrierLabwareString = Location["Carrier Labware String"]
            CarrierTrackStart = Location["Carrier Track Start"]
            CarrierTrackEnd = Location["Carrier Track End"]
            CarrierType = Location["Carrier Type"]
            CarrierPositions = Location["Carrier Positions"]

            DeckLocationInstance = LoadableDeckLocation(
                UniqueIdentifier,
                IsStorageLocation,
                IsPipettableLocation,
                DeckLoadingConfig(
                    CarrierLabwareString,
                    CarrierTrackStart,
                    CarrierTrackEnd,
                    CarrierType,
                    CarrierPositions,
                ),
            )

        else:
            DeckLocationInstance = NonLoadableDeckLocation(
                UniqueIdentifier, IsStorageLocation, IsPipettableLocation
            )

        DeckLocationTrackerInstance.LoadSingle(DeckLocationInstance)

    return DeckLocationTrackerInstance
