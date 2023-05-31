import yaml

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..Backend import BackendTracker
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker, NonPipettableLabware, PipettableLabware
from ..LayoutItem import CoverablePosition, LayoutItemTracker, Lid
from ..TempControlDevice import HamiltonHeaterCooler, HamiltonHeaterShaker
from .BaseTempControlDevice import TempControlDeviceTracker, TempLimits


def LoadYaml(
    BackendTrackerInstance: BackendTracker,
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
            BackendInstance = BackendTrackerInstance.GetObjectByName(
                Device["Backend Unique Identifier"]
            )
            CustomErrorHandling = Device["Custom Error Handling"]
            ComPort = Device["Com Port"]

            StableTempDelta = Device["Temp Limits"]["Stable Delta"]
            MaxTemp = Device["Temp Limits"]["Maximum"]
            MinTemp = Device["Temp Limits"]["Minimum"]
            TempLimitsInstance = TempLimits(StableTempDelta, MinTemp, MaxTemp)
            # Create Temp Config

            DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
                Device["Deck Location Unique Identifier"]
            )

            SupportedLayoutItemTracker = LayoutItemTracker()

            for Labware in Device["Supported Labware Information"]:
                LabwareName = Labware["Plate Labware Unique Identifier"]
                PlateSequence = Labware["Plate Sequence"]
                PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    LabwareName
                )

                if not isinstance(PlateLabwareInstance, PipettableLabware):
                    raise Exception("This should never happen")

                LidSequence = Labware["Lid Sequence"]
                LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    Labware["Lid Labware Unique Identifier"]
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
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be Hamilton Backend")

                TempControlDeviceTrackerInstance.LoadSingle(
                    HamiltonHeaterShaker(
                        UniqueIdentifier,
                        BackendInstance,
                        CustomErrorHandling,
                        ComPort,
                        TempLimitsInstance,
                        SupportedLayoutItemTracker,
                    )
                )

            elif DeviceType == "Hamilton Heater Cooler":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be Hamilton Backend")

                TempControlDeviceTrackerInstance.LoadSingle(
                    HamiltonHeaterCooler(
                        UniqueIdentifier,
                        BackendInstance,
                        CustomErrorHandling,
                        ComPort,
                        TempLimitsInstance,
                        SupportedLayoutItemTracker,
                    )
                )

            else:
                raise Exception("Device type is unknown")

    return TempControlDeviceTrackerInstance
