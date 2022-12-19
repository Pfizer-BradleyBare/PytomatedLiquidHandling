import yaml

from ..TransportDevice.BaseTransportDevice import TransportDeviceTracker
from .DeckLocation import DeckLocation, LoadingConfig
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
                LocationTransportDeviceTrackerInstance.ManualLoad(
                    LocationTransportDevice(
                        TransportDeviceTrackerInstance.GetObjectByName(TransportID),
                        ConfigFile["Location IDs"][LocationID][
                            "Supported Transport IDs"
                        ][TransportID],
                    )
                )

        LoadingConfigInstance = None

        if "Loading" in ConfigFile["Location IDs"][LocationID].keys():
            CarrierString = ConfigFile["Location IDs"][LocationID]["Loading"][
                "Carrier Labware String"
            ]
            CarrierPosition = ConfigFile["Location IDs"][LocationID]["Loading"][
                "Carrier Position"
            ]
            LoadingConfigInstance = LoadingConfig(CarrierString, CarrierPosition)

        DeckLocationTrackerInstance.ManualLoad(
            DeckLocation(
                LocationID,
                LocationTransportDeviceTrackerInstance,
                LoadingConfigInstance,
                ConfigFile["Location IDs"][LocationID]["StorageLocation"],
            )
        )

    return DeckLocationTrackerInstance
