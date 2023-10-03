import logging
import os

import yaml

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import LayoutItem

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from . import HamiltonHeaterCooler, HamiltonHeaterShaker
from .Base import HeatCoolShakeDeviceABC, TempLimits

Logger = logging.getLogger(__name__)


def LoadYaml(
    Backends: dict[str, BackendABC],
    LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC],
    FilePath: str,
) -> dict[str, HeatCoolShakeDeviceABC]:
    Logger.info("Loading TempControlDevice config yaml file.")

    TempControlDevices: dict[str, HeatCoolShakeDeviceABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return TempControlDevices

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return TempControlDevices

    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                Logger.warning(
                    DeviceType
                    + " with unique ID "
                    + Device["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = Device["Identifier"]
            BackendInstance = Backends[Device["Backend Identifier"]]
            CustomErrorHandling = Device["Custom Error Handling"]
            ComPort = Device["Com Port"]

            StableTempDelta = Device["Temp Limits"]["Stable Delta"]
            MaxTemp = Device["Temp Limits"]["Maximum"]
            MinTemp = Device["Temp Limits"]["Minimum"]
            TempLimitsInstance = TempLimits(StableTempDelta, MinTemp, MaxTemp)
            # Create Temp Config

            SupportedLayoutItems: list[LayoutItem.CoverableItem] = list()

            for CoverableLayoutItemUniqueID in Device[
                "Supported Labware Coverable Layout Item Unique Identifiers"
            ]:
                LayoutItemInstance = LayoutItems[CoverableLayoutItemUniqueID]

                if not isinstance(LayoutItemInstance, LayoutItem.CoverableItem):
                    raise Exception("Only coverable layout items are supported")

                SupportedLayoutItems.append(LayoutItemInstance)

            if DeviceType == "Hamilton Heater Shaker":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be Hamilton Backend")

                TempControlDevices[Identifier] = HamiltonHeaterShaker(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ComPort,
                    TempLimitsInstance,
                    SupportedLayoutItems,
                )

            elif DeviceType == "Hamilton Heater Cooler":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be Hamilton Backend")

                TempControlDevices[Identifier] = HamiltonHeaterCooler(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ComPort,
                    TempLimitsInstance,
                    SupportedLayoutItems,
                )

            else:
                raise Exception("Device type is unknown")

    return TempControlDevices
