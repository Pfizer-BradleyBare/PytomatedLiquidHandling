import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..Layout import LayoutItem, LayoutTracker
from .TempControlDevice import DeviceTypes, TempControlDevice, TempLimits
from .TempControlDeviceTracker import TempControlDeviceTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    FilePath: str,
) -> TempControlDeviceTracker:
    TempControlDeviceTrackerInstance = TempControlDeviceTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceID in ConfigFile["Device IDs"]:

        Device = ConfigFile["Device IDs"][DeviceID]

        if Device["Enabled"] is True:

            StableTempDelta = Device["Temp Limits"]["Stable Delta"]
            MaxTemp = Device["Temp Limits"]["Maximum"]
            MinTemp = Device["Temp Limits"]["Minimum"]
            Config = TempLimits(StableTempDelta, MinTemp, MaxTemp)
            # Create Temp Config

            Location = DeckLocationTrackerInstance.GetObjectByName(
                Device["Deck Location ID"]
            )

            LayoutItemTrackerInstance = LayoutTracker()

            for LabwareID in Device["Supported Labware"]:
                Labware = LabwareTrackerInstance.GetObjectByName(LabwareID)

                Sequence = Device["Supported Labware"][LabwareID]["Plate Sequence"]
                LidSequence = Device["Supported Labware"][LabwareID]["Lid Sequence"]

                LayoutItemInstance = LayoutItem(
                    Sequence, LidSequence, Location, Labware
                )

                LayoutItemTrackerInstance.ManualLoad(LayoutItemInstance)
                # add to our list for our item creation and also add it to the layout loader for tracking

            ComPort = Device["Com Port"]
            DeviceType = DeviceTypes(Device["Device Type"])

            TempControlDeviceTrackerInstance.ManualLoad(
                TempControlDevice(
                    DeviceID, ComPort, DeviceType, Config, LayoutItemTrackerInstance
                )
            )

    return TempControlDeviceTrackerInstance
