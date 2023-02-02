import yaml

from ..TransportDevice.BaseTransportDevice import TransportDeviceTracker
from .DeckLoadingConfig.DeckLoadingConfig import CarrierTypes, DeckLoadingConfig
from .DeckLocation import DeckLocation
from .DeckLocationTracker import DeckLocationTracker
from .LocationTransportDevice.LocationTransportDevice import LocationTransportDevice
from .LocationTransportDevice.LocationTransportDeviceTracker import (
    LocationTransportDeviceTracker,
)


def LoadYaml(
    TransportDeviceTrackerInstance: TransportDeviceTracker, FilePath: str
) -> DeckLocationTracker:
    DeckLocationTrackerInstance = DeckLocationTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LocationID in ConfigFile["Location IDs"]:

        LocationTransportDeviceTrackerInstance = LocationTransportDeviceTracker()
        TransportIDs = ConfigFile["Location IDs"][LocationID]["Supported Transport IDs"]

        if TransportIDs is not None:
            for TransportID in TransportIDs:
                print(TransportID)
                LocationTransportDeviceTrackerInstance.ManualLoad(
                    LocationTransportDevice(
                        TransportDeviceTrackerInstance.GetObjectByName(TransportID),
                        ConfigFile["Location IDs"][LocationID][
                            "Supported Transport IDs"
                        ][TransportID],
                    )
                )

        DeckLoadingConfigInstance = None

        if "Deck Loading" in ConfigFile["Location IDs"][LocationID].keys():
            CarrierString = ConfigFile["Location IDs"][LocationID]["Deck Loading"][
                "Carrier Labware String"
            ]
            CarrierTrackStart = ConfigFile["Location IDs"][LocationID]["Deck Loading"][
                "Carrier Track Start"
            ]
            CarrierTrackEnd = ConfigFile["Location IDs"][LocationID]["Deck Loading"][
                "Carrier Track End"
            ]
            CarrierType = CarrierTypes(
                ConfigFile["Location IDs"][LocationID]["Deck Loading"]["Carrier Type"]
            )
            CarrierPositions = ConfigFile["Location IDs"][LocationID]["Deck Loading"][
                "Carrier Positions"
            ]

            DeckLoadingConfigInstance = DeckLoadingConfig(
                CarrierString,
                CarrierTrackStart,
                CarrierTrackEnd,
                CarrierType,
                CarrierPositions,
            )

        DeckLocationTrackerInstance.ManualLoad(
            DeckLocation(
                LocationID,
                LocationTransportDeviceTrackerInstance,
                DeckLoadingConfigInstance,
                ConfigFile["Location IDs"][LocationID]["StorageLocation"],
                ConfigFile["Location IDs"][LocationID]["PipettingLocation"],
            )
        )

    return DeckLocationTrackerInstance
