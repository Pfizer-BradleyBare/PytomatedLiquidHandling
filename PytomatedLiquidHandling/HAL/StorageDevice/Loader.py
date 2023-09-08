import os

import yaml

from PytomatedLiquidHandling.HAL import LayoutItem

from ...Tools.Logger import Logger
from .Base.StorageDeviceABC import StorageDeviceABC
from .RandomAccessDeckStorage import RandomAccessDeckStorage


def LoadYaml(
    LoggerInstance: Logger,
    LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC],
    FilePath: str,
) -> dict[str, StorageDeviceABC]:
    LoggerInstance.info("Loading Storage config yaml file.")

    StorageDevices: dict[str, StorageDeviceABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return StorageDevices

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return StorageDevices

    for StorageTypeID in ConfigFile:
        for Storage in ConfigFile[StorageTypeID]:
            if Storage["Enabled"] == False:
                LoggerInstance.warning(
                    StorageTypeID
                    + " with unique ID "
                    + Storage["Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = Storage["Identifier"]

            if StorageTypeID == "Random Access Deck Storage":
                ItemCount = 0
                ReservableLayoutItems: list[LayoutItem.Base.LayoutItemABC] = list()
                for LayoutItemID in Storage[
                    "Supported Labware Layout Item Identifiers"
                ]:
                    ItemCount += 1
                    ReservableLayoutItems.append(LayoutItems[LayoutItemID])

                StorageInstance = RandomAccessDeckStorage(
                    Identifier, ReservableLayoutItems
                )

            else:
                raise Exception("Storage Type not found. Try agian.")

            StorageDevices[Identifier] = StorageInstance

    return StorageDevices
