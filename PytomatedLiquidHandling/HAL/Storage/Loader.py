import os

import yaml

from PytomatedLiquidHandling.HAL import LayoutItem

from ...Tools.Logger import Logger
from .RandomAccessDeckStorage import RandomAccessDeckStorage
from .StorageTracker import StorageTracker


def LoadYaml(
    LoggerInstance: Logger,
    LayoutItemTrackerInstance: LayoutItem.LayoutItemTracker,
    FilePath: str,
) -> StorageTracker:
    LoggerInstance.info("Loading Storage config yaml file.")

    StorageTrackerInstance = StorageTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return StorageTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return StorageTrackerInstance

    for StorageTypeID in ConfigFile:
        for Storage in ConfigFile[StorageTypeID]:
            if Storage["Enabled"] == False:
                LoggerInstance.warning(
                    StorageTypeID
                    + " with unique ID "
                    + Storage["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
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
