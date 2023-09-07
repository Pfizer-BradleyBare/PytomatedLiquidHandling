import os

import yaml

from PytomatedLiquidHandling.Driver.Hamilton.Backend.BaseHamiltonBackend import (
    HamiltonBackendABC,
)
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware

from ...Tools.Logger import Logger
from . import HamiltonFlipTube, HamiltonFlipTubeSpecial
from .Base import ClosedContainerABC


def LoadYaml(
    LoggerInstance: Logger,
    Backends: dict[str, BackendABC],
    DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC],
    Labwares: dict[str, Labware.Base.LabwareABC],
    FilePath: str,
) -> dict[str, ClosedContainerABC]:
    LoggerInstance.info("Loading ClosedContainer config yaml file.")

    ClosedContainers: dict[str, ClosedContainerABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return ClosedContainers

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return ClosedContainers

    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                LoggerInstance.warning(
                    DeviceType
                    + " with unique ID "
                    + Device["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = Device["Identifier"]
            BackendIdentifier = Device["Backend Identifier"]
            CustomErrorHandling = Device["Custom Error Handling"]

            BackendInstance = Backends[BackendIdentifier]

            SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC] = list()
            for DeckLocationID in Device["Supported Deck Location Identifiers"]:
                SupportedDeckLocations.append(DeckLocations[DeckLocationID])

            SupportedLabwares: list[Labware.Base.LabwareABC] = list()
            for LabwareID in Device["Supported Labware Identifiers"]:
                SupportedLabwares.append(Labwares[LabwareID])

            if DeviceType == "Hamilton FlipTube":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Hamilton FlipTube only accepts Hamilton backends")

                ToolSequence = Device["Tool Sequence"]

                ClosedContainerInstance = HamiltonFlipTube(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ToolSequence,
                    SupportedDeckLocations,
                    SupportedLabwares,
                )

            elif DeviceType == "Hamilton FlipTube Special":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception(
                        "Hamilton FlipTube Special only accepts Hamilton backends"
                    )

                ToolSequence = Device["Tool Sequence"]

                ClosedContainerInstance = HamiltonFlipTubeSpecial(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ToolSequence,
                    SupportedDeckLocations,
                    SupportedLabwares,
                )

            else:
                raise Exception("Device Type not known. Please fix.")

            ClosedContainers[Identifier] = ClosedContainerInstance

    return ClosedContainers
