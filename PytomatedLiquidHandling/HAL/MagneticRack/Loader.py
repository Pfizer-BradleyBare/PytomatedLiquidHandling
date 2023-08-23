import os

import yaml

from PytomatedLiquidHandling.HAL import Backend, LayoutItem, Pipette

from ...Tools.Logger import Logger
from .BaseMagneticRack import MagneticRackABC
from .MagneticRack import MagneticRack


def LoadYaml(
    LoggerInstance: Logger,
    FilePath: str,
    LayoutItems: dict[str, LayoutItem.BaseLayoutItem.LayoutItemABC],
    Pipettes: dict[str, Pipette.BasePipette.Pipette],
) -> dict[str, MagneticRackABC]:
    LoggerInstance.info("Loading MagneticRack config yaml file.")

    MagneticRacks: dict[str, MagneticRackABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return MagneticRacks

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return MagneticRacks

    for Rack in ConfigFile["Rack IDs"]:
        if Rack["Enabled"] == False:
            LoggerInstance.warning(
                "Magnetic Rack"
                + " with unique ID "
                + Rack["Unique Identifier"]
                + " is not enabled so will be skipped."
            )
            continue
        Identifier = Rack["Identifier"]

        SupportedLayoutItems: list[LayoutItem.BaseLayoutItem.LayoutItemABC] = list()

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

            RemoveCategoryInstance = Pipette.BasePipette.LiquidClassCategory(
                Identifier + ": Remove"
            )
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Remove Buffer"]:
                LiquidClassID = LiquidClassInfo["Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                RemoveCategoryInstance.LoadSingle(
                    Pipette.BasePipette.LiquidClass(LiquidClassID, LiquidClassVolume)
                )

            AddCategoryInstance = Pipette.BasePipette.LiquidClassCategory(
                Identifier + ": Add"
            )
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Add Buffer"]:
                LiquidClassID = LiquidClassInfo["Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                AddCategoryInstance.LoadSingle(
                    Pipette.BasePipette.LiquidClass(LiquidClassID, LiquidClassVolume)
                )

            PipetteInstance.SupportedLiquidClassCategoryTrackerInstance.LoadSingle(
                RemoveCategoryInstance
            )
            PipetteInstance.SupportedLiquidClassCategoryTrackerInstance.LoadSingle(
                AddCategoryInstance
            )

        MagneticRacks[Identifier] = MagneticRack(
            Identifier,
            Backend.NullBackend(),
            SupportedLayoutItems,
        )

    return MagneticRacks
