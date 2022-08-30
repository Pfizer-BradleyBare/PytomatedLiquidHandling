import yaml
from .TempControlDevice import TempConfig, TempControlDevice, DeviceTypes
from .TempControlDeviceTracker import TempControlDeviceTracker
from ..Layout import CoveredLayoutItem


def LoadYaml(TempControlDeviceTrackerInstance: TempControlDeviceTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceID in ConfigFile["Device IDs"]:

        Device = ConfigFile["Device IDs"][DeviceID]

        if Device["Enabled"] is True:

            AmbientTemp = Device["Temp Config"]["Ambient"]
            StableTempDelta = Device["Temp Config"]["Stable Delta"]
            MaxTemp = Device["Temp Config"]["Maximum"]
            MinTemp = Device["Temp Config"]["Minimum"]
            Config = TempConfig(AmbientTemp, StableTempDelta, MinTemp, MaxTemp)
            # Create Temp Config

            Location = TempControlDeviceTrackerInstance.DeckLocationTrackerInstance.GetObjectByName(
                Device["Deck Location ID"]
            )

            LayoutItems = list()

            for LabwareID in Device["Supported Labware"]:
                Labware = TempControlDeviceTrackerInstance.LabwareTrackerInstance.GetObjectByName(
                    LabwareID
                )

                Sequence = Device["Supported Labware"][LabwareID]["Plate Sequence"]
                LidSequence = Device["Supported Labware"][LabwareID]["Lid Sequence"]

                LayoutItem = CoveredLayoutItem(Sequence, LidSequence, Location, Labware)

                LayoutItems.append(LayoutItem)
                # add to our list for our item creation and also add it to the layout loader for tracking

            ComPort = Device["Com Port"]
            DeviceType = DeviceTypes(Device["Device Type"])

            TempControlDeviceTrackerInstance.LoadManual(
                TempControlDevice(DeviceID, ComPort, DeviceType, Config, LayoutItems)
            )
