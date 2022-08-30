import yaml
from .Layout import LayoutItem, CoveredLayoutItem
from .LayoutTracker import LayoutTracker as LT


def LoadYaml(LayoutTrackerInstance: LT, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for LabwareID in ConfigFile["Labware IDs"]:
        Items = ConfigFile["Labware IDs"][LabwareID]["Layout Items"]

        if Items is not None:
            for Item in Items:
                Sequence = Item["Deck Sequence"]
                Location = (
                    LayoutTrackerInstance.DeckLocationTrackerInstance.GetObjectByName(
                        Item["Deck Location ID"]
                    )
                )
                LabwareObject = (
                    LayoutTrackerInstance.LabwareTrackerInstance.GetObjectByName(
                        LabwareID
                    )
                )

                if "Lid Sequence" in Item.keys():
                    LidSequence = Item["Lid Sequence"]
                    LayoutTrackerInstance.LoadManual(
                        CoveredLayoutItem(
                            Sequence, LidSequence, Location, LabwareObject
                        )
                    )
                else:
                    LayoutTrackerInstance.LoadManual(
                        LayoutItem(Sequence, Location, LabwareObject)
                    )
                # create item and add to list
