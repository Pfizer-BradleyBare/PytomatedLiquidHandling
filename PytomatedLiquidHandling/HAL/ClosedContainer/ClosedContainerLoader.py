import yaml

from ..Labware import LabwareTracker
from .BaseClosedContainer.ClosedContainerTracker import ClosedContainerTracker
from .FlipTube import FlipTube


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker, FilePath: str
) -> ClosedContainerTracker:
    ClosedContainerTrackerInstance = ClosedContainerTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceID in ConfigFile["Closed Containers Device IDs"]:
        ToolSequence = ConfigFile["Closed Containers Device IDs"][DeviceID][
            "Tool Sequence"
        ]

        SupportedLabwareTrackerInstance = LabwareTracker()
        for LabwareID in ConfigFile["Closed Containers Device IDs"][DeviceID][
            "Supported Labware"
        ]:
            SupportedLabwareTrackerInstance.ManualLoad(
                LabwareTrackerInstance.GetObjectByName(LabwareID)
            )

        ClosedContainerTrackerInstance.ManualLoad(
            FlipTube(ToolSequence, SupportedLabwareTrackerInstance)
        )

    return ClosedContainerTrackerInstance
