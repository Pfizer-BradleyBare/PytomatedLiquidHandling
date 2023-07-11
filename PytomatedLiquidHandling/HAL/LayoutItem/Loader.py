import os

import yaml

from PytomatedLiquidHandling.HAL import DeckLocation, Labware

from ...Tools.Logger import Logger
from .BaseLayoutItem import LayoutItemTracker
from .CoverableItem import CoverableItem
from .Lid import Lid
from .NonCoverableItem import NonCoverableItem


def LoadYaml(
    LoggerInstance: Logger,
    LabwareTrackerInstance: Labware.LabwareTracker,
    DeckLocationTrackerInstance: DeckLocation.DeckLocationTracker,
    FilePath: str,
) -> LayoutItemTracker:
    LoggerInstance.info("Loading LayoutItem config yaml file.")

    LayoutItemTrackerInstance = LayoutItemTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return LayoutItemTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return LayoutItemTrackerInstance

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
                LoggerInstance.warning(
                    LayoutItemID
                    + " with unique ID "
                    + LayoutItem["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            UniqueIdentifier = LayoutItem["Unique Identifier"]
            Sequence = LayoutItem["Sequence"]
            LabwareInstance = LabwareTrackerInstance.GetObjectByName(
                LayoutItem["Labware Unique Identifier"]
            )
            DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
                LayoutItem["Deck Location Unique Identifier"]
            )

            if LayoutItemID == "NonCoverable Item":
                if not isinstance(LabwareInstance, Labware.PipettableLabware):
                    raise Exception("This should not happen")
                # Plates are technically defined here and all plates should be PipettableLabware
                LayoutItemInstance = NonCoverableItem(
                    UniqueIdentifier, Sequence, DeckLocationInstance, LabwareInstance
                )

            elif LayoutItemID == "Coverable Item":
                if not isinstance(LabwareInstance, Labware.PipettableLabware):
                    raise Exception("This should not happen")
                # Plates are technically defined here and all plates should be PipettableLabware
                LidInstance = LayoutItemTrackerInstance.GetObjectByName(
                    LayoutItem["Lid Unique Identifier"]
                )
                if not isinstance(LidInstance, Lid):
                    raise Exception("This lid unique ID is not a lid. Please fix.")

                LayoutItemInstance = CoverableItem(
                    UniqueIdentifier,
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
                    UniqueIdentifier, Sequence, DeckLocationInstance, LabwareInstance
                )

            else:
                raise Exception("Layout item ID not recognized")

            LayoutItemTrackerInstance.LoadSingle(LayoutItemInstance)

    return LayoutItemTrackerInstance
