import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker, NonPipettableLabware, PipettableLabware
from ..LayoutItem import CoverablePosition, LayoutItemTracker, Lid
from ..TempControlDevice import HamiltonHeaterCooler, HamiltonHeaterShaker
from .BaseTempControlDevice import (
    DeviceTypes,
    TempControlDevice,
    TempControlDeviceTracker,
    TempLimits,
)


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
            TempLimitsInstance = TempLimits(StableTempDelta, MinTemp, MaxTemp)
            # Create Temp Config

            SupportedLayoutItemTracker = LayoutItemTracker()

            DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
                Device["Deck Location ID"]
            )

            for LabwareID in Device["Supported Labware"]:
                PlateSequence = Device["Supported Labware"][LabwareID]["Plate Sequence"]
                PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(LabwareID)

                if not isinstance(PlateLabwareInstance, PipettableLabware):
                    raise Exception("This should never happen")

                LidSequence = Device["Supported Labware"][LabwareID]["Lid Sequence"]
                LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    Device["Supported Labware"][LabwareID]["Lid Labware"]
                )

                if not isinstance(LidLabwareInstance, NonPipettableLabware):
                    raise Exception("This should never happen")

                LidInstance = Lid(DeckLocationInstance, LidSequence, LidLabwareInstance)

                LayoutItemInstance = CoverablePosition(
                    DeckLocationInstance,
                    PlateSequence,
                    PlateLabwareInstance,
                    LidInstance,
                )
                SupportedLayoutItemTracker.LoadSingle(LayoutItemInstance)
                # add to our list for our item creation and also add it to the layout loader for tracking

            ComPort = Device["Com Port"]
            DeviceType = DeviceTypes(Device["Device Type"])

            if DeviceType == DeviceTypes.HamiltonHeaterCooler:
                TempControlDeviceTrackerInstance.LoadSingle(
                    HamiltonHeaterCooler(
                        DeviceID,
                        ComPort,
                        TempLimitsInstance,
                        SupportedLayoutItemTracker,
                    )
                )

            if DeviceType == DeviceTypes.HamiltonHeaterShaker:
                TempControlDeviceTrackerInstance.LoadSingle(
                    HamiltonHeaterShaker(
                        DeviceID,
                        ComPort,
                        TempLimitsInstance,
                        SupportedLayoutItemTracker,
                    )
                )

    return TempControlDeviceTrackerInstance
