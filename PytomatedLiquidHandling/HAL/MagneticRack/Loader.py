import os

import yaml

from PytomatedLiquidHandling.HAL import Backend, LayoutItem, Pipette

import logging
from .Base import MagneticRackABC
from .MagneticRack import MagneticRack

Logger = logging.getLogger(__name__)


def LoadYaml(
    FilePath: str,
    LayoutItems: dict[str, LayoutItem.Base.LayoutItemABC],
    Pipettes: dict[str, Pipette.Base.PipetteABC],
) -> dict[str, MagneticRackABC]:
    Logger.info("Loading MagneticRack config yaml file.")

    MagneticRacks: dict[str, MagneticRackABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return MagneticRacks

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return MagneticRacks

    for Rack in ConfigFile["Rack IDs"]:
        if Rack["Enabled"] == False:
            Logger.warning(
                "Magnetic Rack"
                + " with unique ID "
                + Rack["Unique Identifier"]
                + " is not enabled so will be skipped."
            )
            continue
        Identifier = Rack["Identifier"]

        SupportedLayoutItems: list[LayoutItem.Base.LayoutItemABC] = list()

        for LayoutItemUniqueID in Rack["Supported Labware Layout Item Identifiers"]:
            LayoutItemInstance = LayoutItems[LayoutItemUniqueID]

            if isinstance(LayoutItemInstance, LayoutItem.Lid):
                raise Exception(
                    "Only coverable or nonCoverable layout items are supported"
                )

            SupportedLayoutItems.append(LayoutItemInstance)

        for PipetteDevice in Rack["Pipette Identifiers"]:
            PipetteID = PipetteDevice["Identifier"]
            PipetteInstance = Pipettes[PipetteID]

            LiquidClasses: list[Pipette.Base.LiquidClass] = list()
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Remove Buffer"]:
                LiquidClassID = LiquidClassInfo["Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                LiquidClasses.append(
                    Pipette.Base.LiquidClass(LiquidClassID, LiquidClassVolume)
                )
            RemoveCategoryInstance = Pipette.Base.LiquidClassCategory(
                Identifier + ": Remove", LiquidClasses
            )

            LiquidClasses: list[Pipette.Base.LiquidClass] = list()
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Add Buffer"]:
                LiquidClassID = LiquidClassInfo["Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                LiquidClasses.append(
                    Pipette.Base.LiquidClass(LiquidClassID, LiquidClassVolume)
                )
            AddCategoryInstance = Pipette.Base.LiquidClassCategory(
                Identifier + ": Add", LiquidClasses
            )

            PipetteInstance.SupportedLiquidClassCategories.append(
                RemoveCategoryInstance
            )
            PipetteInstance.SupportedLiquidClassCategories.append(AddCategoryInstance)

        MagneticRacks[Identifier] = MagneticRack(
            Identifier,
            Backend.NullBackend(),
            SupportedLayoutItems,
        )

    return MagneticRacks
