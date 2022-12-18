import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..Layout import LayoutItem
from .Lid import Lid
from .LidTracker import LidTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    FilePath: str,
) -> LidTracker:
    LidTrackerInstance = LidTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LidID in ConfigFile["Lid IDs"]:
        LidItem = ConfigFile["Lid IDs"][LidID]

        if LidItem["Enabled"] is True:

            LidLabware = LabwareTrackerInstance.GetObjectByName(LidItem["Labware"])
            LidLocation = DeckLocationTrackerInstance.GetObjectByName(
                LidItem["Deck Location ID"]
            )
            LidSequence = LidItem["Sequence"]

            SupportedLabwareTrackerInstance = LabwareTracker()

            for LabwareID in LidItem["Supported Labware"]:
                SupportedLabwareTrackerInstance.ManualLoad(
                    LabwareTrackerInstance.GetObjectByName(LabwareID)
                )

            LidTrackerInstance.ManualLoad(
                Lid(
                    LidID,
                    LayoutItem(LidSequence, None, LidLocation, LidLabware),
                    SupportedLabwareTrackerInstance,
                )
            )
            # Create Labware Class and append

    return LidTrackerInstance
