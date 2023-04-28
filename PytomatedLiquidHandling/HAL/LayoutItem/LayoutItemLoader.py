import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..LayoutItem import CoverablePosition, LayoutItemTracker, Lid, UncoverablePosition


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

    for DeckLocationID in ConfigFile["DeckLocation IDs"]:
        DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
            DeckLocationID
        )

        for Item in ConfigFile["DeckLocation IDs"][DeckLocationID]:
            PlateSequence = Item["Plate Sequence"]
            PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                Item["Plate Labware"]
            )

            if "Lid Sequence" in Item:
                LidSequence = Item["Lid Sequence"]
                LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    Item["Lid Labware"]
                )

                LidInstance = Lid(DeckLocationInstance, LidSequence, LidLabwareInstance)
                LayoutItemInstance = CoverablePosition(
                    DeckLocationInstance,
                    PlateSequence,
                    PlateLabwareInstance,
                    LidInstance,
                )

            else:
                LayoutItemInstance = UncoverablePosition(
                    DeckLocationInstance, PlateSequence, PlateLabwareInstance
                )

            LayoutItemTrackerInstance.ManualLoad(LayoutItemInstance)

    print("DONE")
    return LayoutItemTrackerInstance
