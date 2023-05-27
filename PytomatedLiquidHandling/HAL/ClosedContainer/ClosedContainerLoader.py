import yaml

from ..ClosedContainer import HamiltonFlipTube, HamiltonFlipTubeSpecial
from ..Labware import LabwareTracker
from ..DeckLocation import DeckLocationTracker
from .BaseClosedContainer import ClosedContainerTracker
from ..Backend import BackendTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


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
            BackendIdentifier = Device["Backend Identifier"]
            CustomErrorHandling = Device["Custom Error Handling"]

            BackendInstance = BackendTrackerInstance.GetObjectByName(BackendIdentifier)

            SupportedDeckLocationTrackerInstance = DeckLocationTracker()
            for DeckLocationID in Device["Supported Deck Locations"]:
                SupportedDeckLocationTrackerInstance.LoadSingle(
                    SupportedDeckLocationTrackerInstance.GetObjectByName(DeckLocationID)
                )

            SupportedLabwareTrackerInstance = LabwareTracker()
            for LabwareID in Device["Supported Labware"]:
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
