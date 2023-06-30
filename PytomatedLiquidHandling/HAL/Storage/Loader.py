import yaml

from PytomatedLiquidHandling.HAL import LayoutItem

from . import RandomAccessDeckStorage, StorageTracker


def LoadYaml(
    LayoutItemTrackerInstance: LayoutItem.LayoutItemTracker,
    FilePath: str,
) -> StorageTracker:
    StorageTrackerInstance = StorageTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for StorageTypeID in ConfigFile:
        for Storage in ConfigFile[StorageTypeID]:
            if Storage["Enabled"] == False:
                continue

            UniqueIdentifier = Storage["Unique Identifier"]

            if StorageTypeID == "Random Access Deck Storage":
                ItemCount = 0
                ReservableItemTrackerInstance = LayoutItem.LayoutItemTracker()
                for LayoutItemUniqueID in Storage[
                    "Supported Labware Layout Item Unique Identifiers"
                ]:
                    ItemCount += 1
                    ReservableItemTrackerInstance.LoadSingle(
                        LayoutItemTrackerInstance.GetObjectByName(LayoutItemUniqueID)
                    )

                StorageInstance = RandomAccessDeckStorage(
                    UniqueIdentifier, ReservableItemTrackerInstance
                )

            else:
                raise Exception("Storage Type not found. Try agian.")

            StorageTrackerInstance.LoadSingle(StorageInstance)

    return StorageTrackerInstance
