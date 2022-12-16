import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .LayoutItem import LayoutItem
from .LayoutItemTracker import LayoutItemTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    FilePath: str,
) -> LayoutItemTracker:

    LayoutItemTrackerInstance = LayoutItemTracker()

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

                LayoutItemTrackerInstance.ManualLoad(
                    LayoutItem(Sequence, LidSequence, Location, LabwareObject)
                )
                # create item and add to list

    return LayoutItemTrackerInstance
