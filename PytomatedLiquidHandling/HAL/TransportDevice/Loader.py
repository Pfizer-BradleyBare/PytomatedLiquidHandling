import os

import yaml

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    HamiltonBackendABC,
    VantageBackend,
)
from PytomatedLiquidHandling.HAL import Backend, Labware

from ...Tools.Logger import Logger

from .Base import TransportDeviceABC
from .HamiltonCOREGripper import HamiltonCOREGripper
from .HamiltonInternalPlateGripper import HamiltonInternalPlateGripper
from .VantageTrackGripper import VantageTrackGripper


def LoadYaml(
    LoggerInstance: Logger,
    Backends: dict[str, Backend.Base.BackendABC],
    Labwares: dict[str, Labware.Base.LabwareABC],
    FilePath: str,
) -> dict[str, TransportDeviceABC]:
    LoggerInstance.info("Loading TransportDevice config yaml file.")

    TransportDevices: dict[str, TransportDeviceABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return TransportDevices

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return TransportDevices

    for DeviceType in ConfigFile:
        Device = ConfigFile[DeviceType]

        if Device["Enabled"] == False:
            LoggerInstance.warning(
                DeviceType
                + " with unique ID "
                + Device["Identifier"]
                + " is not enabled so will be skipped."
            )
            continue

        UniqueIdentifier = Device["Identifier"]
        BackendInstance = Backends[Device["Backend Identifier"]]
        CustomErrorHandling = Device["Custom Error Handling"]

        SupportedLabwares: list[Labware.Base.LabwareABC] = list()
        for LabwareID in Device["Supported Labware Identifiers"]:
            SupportedLabwares.append(Labwares[LabwareID])

        if DeviceType == "Hamilton CORE Gripper":
            GripperSequence = Device["Gripper Sequence"]

            if not isinstance(BackendInstance, HamiltonBackendABC):
                raise Exception("Backend not correct. Must be of Hamilton backend type")

            TransportDevices[UniqueIdentifier] = HamiltonCOREGripper(
                UniqueIdentifier,
                BackendInstance,
                CustomErrorHandling,
                SupportedLabwares,
                GripperSequence,
            )

        elif DeviceType == "Hamilton Internal Plate Gripper":
            if not isinstance(BackendInstance, HamiltonBackendABC):
                raise Exception("Backend not correct. Must be of Hamilton backend type")

            TransportDevices[UniqueIdentifier] = HamiltonInternalPlateGripper(
                UniqueIdentifier,
                BackendInstance,
                CustomErrorHandling,
                SupportedLabwares,
            )

        elif DeviceType == "Vantage Track Gripper":
            if not isinstance(BackendInstance, VantageBackend):
                raise Exception("Backend not correct. Must be of Vantage backend type")

            TransportDevices[UniqueIdentifier] = VantageTrackGripper(
                UniqueIdentifier,
                BackendInstance,
                CustomErrorHandling,
                SupportedLabwares,
            )

    return TransportDevices
