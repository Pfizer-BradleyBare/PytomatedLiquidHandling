import yaml

from ..ClosedContainer import HamiltonFlipTube, HamiltonFlipTubeSpecial
from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainerTracker
from ..Backend import BackendTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


def LoadYaml(
    BackendTrackerInstance: BackendTracker,
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

            if DeviceType == "Hamilton FlipTube":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Hamilton FlipTube only accepts Hamilton backends")

                ToolSequence = Device["Tool Sequence"]

                SupportedLabwareTrackerInstance = LabwareTracker()
                for LabwareID in Device["Supported Labware"]:
                    SupportedLabwareTrackerInstance.LoadSingle(
                        LabwareTrackerInstance.GetObjectByName(LabwareID)
                    )

                ClosedContainerInstance = HamiltonFlipTube(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ToolSequence,
                    SupportedLabwareTrackerInstance,
                )

            elif DeviceType == "Hamilton FlipTube Special":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception(
                        "Hamilton FlipTube Special only accepts Hamilton backends"
                    )

                ToolSequence = Device["Tool Sequence"]

                SupportedLabwareTrackerInstance = LabwareTracker()
                for LabwareID in Device["Supported Labware"]:
                    SupportedLabwareTrackerInstance.LoadSingle(
                        LabwareTrackerInstance.GetObjectByName(LabwareID)
                    )

                ClosedContainerInstance = HamiltonFlipTubeSpecial(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    ToolSequence,
                    SupportedLabwareTrackerInstance,
                )

            else:
                raise Exception("Device Type not known. Please fix.")

            ClosedContainerTrackerInstance.LoadSingle(ClosedContainerInstance)

    return ClosedContainerTrackerInstance
