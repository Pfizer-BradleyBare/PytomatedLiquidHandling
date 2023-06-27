import yaml

from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker, NonPipettableLabware
from . import LidStorageTracker, RandomAccessLidStorage
from ..LayoutItem import Lid, LayoutItemTracker


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker,
    DeckLocationTrackerInstance: DeckLocationTracker,
    FilePath: str,
) -> LidStorageTracker:
    LidStorageTrackerInstance = LidStorageTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for StorageTypeID in ConfigFile:
        for Storage in ConfigFile[StorageTypeID]:
            if Storage["Enabled"] == False:
                continue

            UniqueIdentifier = Storage["Unique Identifier"]

            if StorageTypeID == "Random Access Lid Storage":
                LidLabwareInstance = LabwareTrackerInstance.GetObjectByName(
                    Storage["Lid Labware"]
                )

                if not isinstance(LidLabwareInstance, NonPipettableLabware):
                    raise Exception("Wrong labware")

                LidCount = 1
                ReservableLidTrackerInstance = LayoutItemTracker()
                for LidPosition in Storage["Lid Positions"]:
                    Sequence = LidPosition["Sequence"]
                    DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
                        LidPosition["Deck Location"]
                    )

                    ReservableLidTrackerInstance.LoadSingle(
                        Lid(
                            StorageTypeID + " -> Lid Position #" + str(LidCount),
                            Sequence,
                            DeckLocationInstance,
                            LidLabwareInstance,
                        )
                    )

                LidStorageInstance = RandomAccessLidStorage(
                    UniqueIdentifier, ReservableLidTrackerInstance
                )

            else:
                raise Exception("Storage Type not found. Try agian.")

            LidStorageTrackerInstance.LoadSingle(LidStorageInstance)

    return LidStorageTrackerInstance
