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

    for DeviceType in ConfigFile:

        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                continue

            UniqueIdentifier = Device["Unique Identifier"]
            ComPort = Device["Com Port"]

            StableTempDelta = Device["Temp Limits"]["Stable Delta"]
            MaxTemp = Device["Temp Limits"]["Maximum"]
            MinTemp = Device["Temp Limits"]["Minimum"]
            TempLimitsInstance = TempLimits(StableTempDelta, MinTemp, MaxTemp)
            # Create Temp Config

            DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
                Device["Deck Location ID"]
            )

            SupportedLayoutItemTracker = LayoutItemTracker()

            for Labware in Device["Supported Labware"]:
                LabwareName = Labware["Labware"]
                PlateSequence = Labware["Plate Sequence"]
                PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    LabwareName
                )

                if not isinstance(PlateLabwareInstance, PipettableLabware):
                    raise Exception("This should never happen")

                LidSequence = Labware["Lid Sequence"]
                LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    Labware["Lid Labware"]
                )

                if not isinstance(LidLabwareInstance, NonPipettableLabware):
                    raise Exception("This should never happen")

                LidInstance = Lid(
                    UniqueIdentifier + " " + LabwareName + " Lid",
                    LidSequence,
                    LidLabwareInstance,
                    DeckLocationInstance,
                )

                LayoutItemInstance = CoverablePosition(
                    UniqueIdentifier + " " + LabwareName,
                    PlateSequence,
                    PlateLabwareInstance,
                    DeckLocationInstance,
                    LidInstance,
                )
                SupportedLayoutItemTracker.LoadSingle(LayoutItemInstance)
                # add to our list for our item creation and also add it to the layout loader for tracking

            if DeviceType == "Hamilton Heater Shaker":
                TempControlDeviceTrackerInstance.LoadSingle(
                    HamiltonHeaterShaker(
                        UniqueIdentifier,
                        ComPort,
                        TempLimitsInstance,
                        SupportedLayoutItemTracker,
                    )
                )

            elif DeviceType == "Hamilton Heater Cooler":
                TempControlDeviceTrackerInstance.LoadSingle(
                    HamiltonHeaterCooler(
                        UniqueIdentifier,
                        ComPort,
                        TempLimitsInstance,
                        SupportedLayoutItemTracker,
                    )
                )

            else:
                raise Exception("Device type is unknown")

    return TempControlDeviceTrackerInstance
