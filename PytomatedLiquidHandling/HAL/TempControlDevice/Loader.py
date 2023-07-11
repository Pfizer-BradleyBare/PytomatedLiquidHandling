import os

import yaml

from PytomatedLiquidHandling.HAL import Backend, LayoutItem

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from . import HamiltonHeaterCooler, HamiltonHeaterShaker
from .BaseTempControlDevice import TempControlDeviceTracker, TempLimits


def LoadYaml(
    LoggerInstance: Logger,
    BackendTrackerInstance: Backend.BackendTracker,
    LayoutItemTrackerInstance: LayoutItem.LayoutItemTracker,
    FilePath: str,
) -> TempControlDeviceTracker:
    TempControlDeviceTrackerInstance = TempControlDeviceTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("TempControlDevice config file does not exist.")
        return TempControlDeviceTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "TempControlDevice config file exists but does not contain any config items"
        )
        return TempControlDeviceTrackerInstance

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

            SupportedLayoutItemTracker = LayoutItem.LayoutItemTracker()

            for CoverableLayoutItemUniqueID in Device[
                "Supported Labware Coverable Layout Item Unique Identifiers"
            ]:
                LayoutItemInstance = LayoutItemTrackerInstance.GetObjectByName(
                    CoverableLayoutItemUniqueID
                )

                if not isinstance(LayoutItemInstance, LayoutItem.CoverableItem):
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
