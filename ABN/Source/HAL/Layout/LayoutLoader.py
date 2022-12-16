import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .Layout import LayoutItem
from .LayoutTracker import LayoutTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    FilePath: str,
) -> LayoutTracker:

    LayoutTrackerInstance = LayoutTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LabwareID in ConfigFile["Labware IDs"]:
        Items = ConfigFile["Labware IDs"][LabwareID]["Layout Items"]

        if Items is not None:
            for Item in Items:
                Sequence = Item["Deck Sequence"]
                Location = DeckLocationTrackerInstance.GetObjectByName(
                    Item["Deck Location ID"]
                )
                LabwareObject = LabwareTrackerInstance.GetObjectByName(LabwareID)

                LidSequence = None
                if "Lid Sequence" in Item.keys():
                    LidSequence = Item["Lid Sequence"]

                LayoutTrackerInstance.ManualLoad(
                    LayoutItem(Sequence, LidSequence, Location, LabwareObject)
                )
                # create item and add to list

    return LayoutTrackerInstance
