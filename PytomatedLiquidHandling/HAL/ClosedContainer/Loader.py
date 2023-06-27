import yaml

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..Backend import BackendTracker
from . import HamiltonFlipTube, HamiltonFlipTubeSpecial
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainerTracker


def LoadYaml(
    BackendTrackerInstance: BackendTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    LabwareTrackerInstance: LabwareTracker,
    FilePath: str,
) -> ClosedContainerTracker:
    ClosedContainerTrackerInstance = ClosedContainerTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceType in ConfigFile:
        for Device in ConfigFile[DeviceType]:
            if Device["Enabled"] == False:
                continue

            UniqueIdentifier = Device["Unique Identifier"]
            BackendIdentifier = Device["Backend Unique Identifier"]
            CustomErrorHandling = Device["Custom Error Handling"]

            BackendInstance = BackendTrackerInstance.GetObjectByName(BackendIdentifier)

            SupportedDeckLocationTrackerInstance = DeckLocationTracker()
            for DeckLocationID in Device["Supported Deck Location Unique Identifiers"]:
                SupportedDeckLocationTrackerInstance.LoadSingle(
                    DeckLocationTrackerInstance.GetObjectByName(DeckLocationID)
                )

            SupportedLabwareTrackerInstance = LabwareTracker()
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
