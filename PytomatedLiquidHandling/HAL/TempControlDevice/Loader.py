import yaml

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..Backend import BackendTracker
from ..LayoutItem import CoverableItem, LayoutItemTracker
from . import HamiltonHeaterCooler, HamiltonHeaterShaker
from .BaseTempControlDevice import TempControlDeviceTracker, TempLimits


def LoadYaml(
    BackendTrackerInstance: BackendTracker,
    LayoutItemTrackerInstance: LayoutItemTracker,
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

            SupportedLayoutItemTracker = LayoutItemTracker()

            for CoverableLayoutItemUniqueID in Device[
                "Supported Labware Coverable Layout Item Unique Identifiers"
            ]:
                LayoutItemInstance = LayoutItemTrackerInstance.GetObjectByName(
                    CoverableLayoutItemUniqueID
                )

                if not isinstance(LayoutItemInstance, CoverableItem):
                    raise Exception("Only coverable layout items are supported")

                SupportedLayoutItemTracker.LoadSingle(LayoutItemInstance)

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
