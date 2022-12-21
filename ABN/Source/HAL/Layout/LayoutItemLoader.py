import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .LayoutItem.LayoutItem import LayoutItem
from .LayoutItemGrouping import LayoutItemGrouping
from .LayoutItemGroupingTracker import LayoutItemGroupingTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    FilePath: str,
) -> LayoutItemGroupingTracker:

    LayoutItemGroupingTrackerInstance = LayoutItemGroupingTracker()

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

            PlateLayoutItemInstance = LayoutItem(
                PlateSequence, DeckLocationInstance, PlateLabwareInstance
            )
            LidLayoutItemInstance: LayoutItem | None = None

            if "Lid Sequence" in Item:
                LidSequence = Item["Lid Sequence"]
                LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    Item["Lid Labware"]
                )

                LidLayoutItemInstance = LayoutItem(
                    LidSequence, DeckLocationInstance, LidLabwareInstance
                )

            LayoutItemGroupingTrackerInstance.ManualLoad(
                LayoutItemGrouping(PlateLayoutItemInstance, LidLayoutItemInstance)
            )

    print("DONE")
    return LayoutItemGroupingTrackerInstance
