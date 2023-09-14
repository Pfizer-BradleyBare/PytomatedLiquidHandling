import os

import yaml

from PytomatedLiquidHandling.HAL import DeckLocation, Labware

import logging
from .Base import LayoutItemABC
from .CoverableItem import CoverableItem
from .Lid import Lid
from .NonCoverableItem import NonCoverableItem

Logger = logging.getLogger(__name__)


def LoadYaml(
    Labwares: dict[str, Labware.Base.LabwareABC],
    DeckLocations: dict[str, DeckLocation.Base.DeckLocationABC],
    FilePath: str,
) -> dict[str, LayoutItemABC]:
    Logger.info("Loading LayoutItem config yaml file.")

    LayoutItems: dict[str, LayoutItemABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return LayoutItems

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return LayoutItems

    OldConfigFile = ConfigFile
    ConfigFile = dict()

    if "Coverable Item" in OldConfigFile:
        if "Lid" not in OldConfigFile:
            raise Exception(
                "You are defining Coverable items but not lids. Lids are required for coverable items."
            )
        ConfigFile["Lid"] = OldConfigFile["Lid"]
        ConfigFile["Coverable Item"] = OldConfigFile["Coverable Item"]

    if "NonCoverable Item" in OldConfigFile:
        ConfigFile["NonCoverable Item"] = OldConfigFile["NonCoverable Item"]
    # Reorder input config as needed

    for LayoutItemID in ConfigFile:
        for LayoutItem in ConfigFile[LayoutItemID]:
            if LayoutItem["Enabled"] == False:
                Logger.warning(
                    LayoutItemID
                    + " with unique ID "
                    + LayoutItem["Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = LayoutItem["Identifier"]
            Sequence = LayoutItem["Sequence"]
            LabwareInstance = Labwares[LayoutItem["Labware Identifier"]]
            DeckLocationInstance = DeckLocations[LayoutItem["Deck Location Identifier"]]

            if LayoutItemID == "NonCoverable Item":
                if not isinstance(LabwareInstance, Labware.PipettableLabware):
                    raise Exception("This should not happen")
                # Plates are technically defined here and all plates should be PipettableLabware
                LayoutItemInstance = NonCoverableItem(
                    Identifier, Sequence, DeckLocationInstance, LabwareInstance
                )

            elif LayoutItemID == "Coverable Item":
                if not isinstance(LabwareInstance, Labware.PipettableLabware):
                    raise Exception("This should not happen")
                # Plates are technically defined here and all plates should be PipettableLabware
                LidInstance = LayoutItems[LayoutItem["Lid Identifier"]]
                if not isinstance(LidInstance, Lid):
                    raise Exception("This lid unique ID is not a lid. Please fix.")

                LayoutItemInstance = CoverableItem(
                    Identifier,
                    Sequence,
                    DeckLocationInstance,
                    LabwareInstance,
                    LidInstance,
                )

            elif LayoutItemID == "Lid":
                if not isinstance(LabwareInstance, Labware.NonPipettableLabware):
                    raise Exception("This should not happen")
                # Lids are obviously NonPipettableLabware
                LayoutItemInstance = Lid(
                    Identifier, Sequence, DeckLocationInstance, LabwareInstance
                )

            else:
                raise Exception("Layout item ID not recognized")

            LayoutItems[Identifier] = LayoutItemInstance

    return LayoutItems
