import yaml

from ..Labware import LabwareTracker
from .FlipTube import FlipTube
from .FlipTubeTracker import FlipTubeTracker


def LoadYaml(LabwareTrackerInstance: LabwareTracker, FilePath: str) -> FlipTubeTracker:
    FlipTubeTrackerInstance = FlipTubeTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for FlipTubeID in ConfigFile["FlipTube Tool IDs"]:
        Sequence = ConfigFile["FlipTube Tool IDs"][FlipTubeID]["Sequence"]

        if ConfigFile["FlipTube Tool IDs"][FlipTubeID]["Supported Labware"] is None:
            continue

        SupportedLabwareTrackerInstance = LabwareTracker()
        for LabwareID in ConfigFile["FlipTube Tool IDs"][FlipTubeID][
            "Supported Labware"
        ]:
            SupportedLabwareTrackerInstance.ManualLoad(
                LabwareTrackerInstance.GetObjectByName(LabwareID)
            )

        FlipTubeTrackerInstance.ManualLoad(
            FlipTube(FlipTubeID, Sequence, SupportedLabwareTrackerInstance)
        )

    return FlipTubeTrackerInstance
