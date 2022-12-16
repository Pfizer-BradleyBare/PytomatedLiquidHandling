import yaml

from ..Transport.BaseTransportDevice import TransportDeviceTracker
from .DeckLocation import DeckLocation, LoadingConfig
from .DeckLocationTracker import DeckLocationTracker


def LoadYaml(
    TransportDeviceTrackerInstance: TransportDeviceTracker, FilePath: str
) -> DeckLocationTracker:
    DeckLocationTrackerInstance = DeckLocationTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LocationID in ConfigFile["Location IDs"]:

        TransportDevices = list()
        TransportIDs = ConfigFile["Location IDs"][LocationID]["Supported Transport IDs"]

        if TransportIDs is not None:
            for TransportID in TransportIDs:
                TransportDevices.append(
                    TransportDeviceTrackerInstance.GetObjectByName(TransportID)
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
                TransportDevices,
                LoadingConfigInstance,
                ConfigFile["Location IDs"][LocationID]["StorageLocation"],
            )
        )

    return DeckLocationTrackerInstance
