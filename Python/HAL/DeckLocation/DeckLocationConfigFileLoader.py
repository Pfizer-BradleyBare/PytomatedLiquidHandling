import yaml
from .DeckLocation import DeckLocation, LoadableDeckLocation, LoadingConfig
from .DeckLocationTracker import DeckLocationTracker


def LoadYaml(DeckLocationTrackerInstance: DeckLocationTracker, FilePath: str):
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
                    DeckLocationTrackerInstance.TransportTrackerInstance.GetObjectByName(
                        TransportID
                    )
                )

        if "Loading" in ConfigFile["Location IDs"][LocationID].keys():
            CarrierString = ConfigFile["Location IDs"][LocationID]["Loading"][
                "Carrier Labware String"
            ]
            CarrierPosition = ConfigFile["Location IDs"][LocationID]["Loading"][
                "Carrier Position"
            ]
            DeckLocationTrackerInstance.LoadManual(
                LoadableDeckLocation(
                    LocationID,
                    TransportDevices,
                    LoadingConfig(CarrierString, CarrierPosition),
                )
            )
        else:
            DeckLocationTrackerInstance.LoadManual(
                DeckLocation(LocationID, TransportDevices)
            )
