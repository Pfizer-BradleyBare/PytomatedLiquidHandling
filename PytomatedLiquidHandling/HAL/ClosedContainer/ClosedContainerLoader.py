import yaml

from ..ClosedContainer import HamiltonFlipTube, HamiltonFlipTubeSpecial
from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainerTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker, FilePath: str
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

            UniqueName = Device["Unique Name"]

            if DeviceType == "Hamilton FlipTube":
                ToolSequence = Device["Tool Sequence"]

                SupportedLabwareTrackerInstance = LabwareTracker()
                for LabwareID in Device["Supported Labware"]:
                    SupportedLabwareTrackerInstance.LoadSingle(
                        LabwareTrackerInstance.GetObjectByName(LabwareID)
                    )

                ClosedContainerInstance = HamiltonFlipTube(
                    UniqueName, ToolSequence, SupportedLabwareTrackerInstance
                )

            elif DeviceType == "Hamilton FlipTube Special":
                ToolSequence = Device["Tool Sequence"]

                SupportedLabwareTrackerInstance = LabwareTracker()
                for LabwareID in Device["Supported Labware"]:
                    SupportedLabwareTrackerInstance.LoadSingle(
                        LabwareTrackerInstance.GetObjectByName(LabwareID)
                    )

                ClosedContainerInstance = HamiltonFlipTubeSpecial(
                    UniqueName, ToolSequence, SupportedLabwareTrackerInstance
                )

            else:
                raise Exception("Device Type not known. Please fix.")

            ClosedContainerTrackerInstance.LoadSingle(ClosedContainerInstance)

    return ClosedContainerTrackerInstance
