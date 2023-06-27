import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker, NonPipettableLabware, PipettableLabware
from . import CoverablePosition, LayoutItemTracker, Lid, NonCoverablePosition


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

    for LayoutItem in ConfigFile:
        if LayoutItem["Enabled"] == False:
            continue
        UniqueIdentifier = LayoutItem["Unique Identifier"]
        PlateSequence = LayoutItem["Plate Sequence"]
        PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(
            LayoutItem["Plate Labware Unique Identifier"]
        )
        DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
            LayoutItem["Deck Location Unique Identifier"]
        )

        if not isinstance(PlateLabwareInstance, PipettableLabware):
            raise Exception("This should not happen")
        # Plates are technically defined here and all plates should be PipettableLabware

        if "Lid Sequence" in LayoutItem:
            LidSequence = LayoutItem["Lid Sequence"]
            LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                LayoutItem["Lid Labware Unique Identifier"]
            )

            if not isinstance(LidLabwareInstance, NonPipettableLabware):
                raise Exception("This should not happen")
            # Lids are obviously NonPipettableLabware

            LayoutItemInstance = CoverablePosition(
                UniqueIdentifier,
                PlateSequence,
                DeckLocationInstance,
                PlateLabwareInstance,
                Lid(
                    UniqueIdentifier,
                    LidSequence,
                    DeckLocationInstance,
                    LidLabwareInstance,
                ),
            )

        else:
            LayoutItemInstance = NonCoverablePosition(
                UniqueIdentifier,
                PlateSequence,
                DeckLocationInstance,
                PlateLabwareInstance,
            )

        LayoutItemTrackerInstance.LoadSingle(LayoutItemInstance)

    return LayoutItemTrackerInstance
