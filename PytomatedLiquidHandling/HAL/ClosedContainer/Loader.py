import os

import yaml

from PytomatedLiquidHandling.HAL import DeckLocation, Labware

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from ..Backend import BackendTracker
from . import HamiltonFlipTube, HamiltonFlipTubeSpecial
from .BaseClosedContainer import ClosedContainerTracker


def LoadYaml(
    LoggerInstance: Logger,
    BackendTrackerInstance: BackendTracker,
    DeckLocationTrackerInstance: DeckLocation.DeckLocationTracker,
    LabwareTrackerInstance: Labware.LabwareTracker,
    FilePath: str,
) -> ClosedContainerTracker:
    ClosedContainerTrackerInstance = ClosedContainerTracker()

    if not os.path.exists(FilePath):
        return ClosedContainerTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        return ClosedContainerTrackerInstance

    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                continue

            UniqueIdentifier = Device["Unique Identifier"]
            BackendIdentifier = Device["Backend Unique Identifier"]
            CustomErrorHandling = Device["Custom Error Handling"]

            BackendInstance = BackendTrackerInstance.GetObjectByName(BackendIdentifier)

            SupportedDeckLocationTrackerInstance = DeckLocation.DeckLocationTracker()
            for DeckLocationID in Device["Supported Deck Location Unique Identifiers"]:
                SupportedDeckLocationTrackerInstance.LoadSingle(
                    DeckLocationTrackerInstance.GetObjectByName(DeckLocationID)
                )

            SupportedLabwareTrackerInstance = Labware.LabwareTracker()
            for LabwareID in Device["Supported Labware Unique Identifiers"]:
                SupportedLabwareTrackerInstance.LoadSingle(
                    LabwareTrackerInstance.GetObjectByName(LabwareID)
                )

            if DeviceType == "Hamilton FlipTube":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Hamilton FlipTube only accepts Hamilton backends")

                ToolSequence = Device["Tool Sequence"]

                ClosedContainerInstance = HamiltonFlipTube(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ToolSequence,
                    SupportedDeckLocationTrackerInstance,
                    SupportedLabwareTrackerInstance,
                )

            elif DeviceType == "Hamilton FlipTube Special":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception(
                        "Hamilton FlipTube Special only accepts Hamilton backends"
                    )

                ToolSequence = Device["Tool Sequence"]

                ClosedContainerInstance = HamiltonFlipTubeSpecial(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ToolSequence,
                    SupportedDeckLocationTrackerInstance,
                    SupportedLabwareTrackerInstance,
                )

            else:
                raise Exception("Device Type not known. Please fix.")

            ClosedContainerTrackerInstance.LoadSingle(ClosedContainerInstance)

    return ClosedContainerTrackerInstance
