import yaml

from ..Labware import LabwareTracker
from .BaseClosedContainer import ClosedContainerTracker, ClosedContainerTypes
from .HamiltonFlipTube import HamiltonFlipTube


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker, FilePath: str
) -> ClosedContainerTracker:
    ClosedContainerTrackerInstance = ClosedContainerTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceType in ConfigFile["Closed Container Device Types"]:
        for Device in ConfigFile["Closed Container Device Types"][DeviceType]:
            UniqueName = Device["Unique Name"]

            if DeviceType == ClosedContainerTypes.HamiltonFlipTube.value:
                ToolSequence = Device["Tool Sequence"]

                SupportedLabwareTrackerInstance = LabwareTracker()
                for LabwareID in Device["Supported Labware"]:
                    SupportedLabwareTrackerInstance.ManualLoad(
                        LabwareTrackerInstance.GetObjectByName(LabwareID)
                    )

                ClosedContainerTrackerInstance.ManualLoad(
                    HamiltonFlipTube(
                        UniqueName, ToolSequence, SupportedLabwareTrackerInstance
                    )
                )

    return ClosedContainerTrackerInstance
