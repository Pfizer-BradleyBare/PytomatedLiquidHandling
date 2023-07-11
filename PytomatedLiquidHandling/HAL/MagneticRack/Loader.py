import os

import yaml

from PytomatedLiquidHandling.HAL import Backend, LayoutItem, Pipette

from ...Tools.Logger import Logger
from .BaseMagneticRack import MagneticRackTracker
from .MagneticRack import MagneticRack


def LoadYaml(
    LoggerInstance: Logger,
    FilePath: str,
    LayoutItemTrackerInstance: LayoutItem.LayoutItemTracker,
    PipetteTrackerInstance: Pipette.PipetteTracker,
) -> MagneticRackTracker:
    LoggerInstance.info("Loading MagneticRack config yaml file.")

    MagneticRackTrackerInstance = MagneticRackTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return MagneticRackTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return MagneticRackTrackerInstance

    for Rack in ConfigFile["Rack IDs"]:
        if Rack["Enabled"] == False:
            LoggerInstance.warning(
                "Magnetic Rack"
                + " with unique ID "
                + Rack["Unique Identifier"]
                + " is not enabled so will be skipped."
            )
            continue
        UniqueIdentifier = Rack["Unique Identifier"]

        SupportedLayoutItemTrackerInstance = LayoutItem.LayoutItemTracker()

        for LayoutItemUniqueID in Rack[
            "Supported Labware Layout Item Unique Identifiers"
        ]:
            LayoutItemInstance = LayoutItemTrackerInstance.GetObjectByName(
                LayoutItemUniqueID
            )

            if isinstance(LayoutItemInstance, LayoutItem.Lid):
                raise Exception(
                    "Only coverable or nonCoverable layout items are supported"
                )

            SupportedLayoutItemTrackerInstance.LoadSingle(LayoutItemInstance)

        for PipetteDevice in Rack["Pipette Unique Identifiers"]:
            PipetteID = PipetteDevice["Unique Identifier"]
            PipetteInstance = PipetteTrackerInstance.GetObjectByName(PipetteID)

            RemoveCategoryInstance = Pipette.BasePipette.LiquidClassCategory(
                UniqueIdentifier + ": Remove"
            )
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Remove Buffer"]:
                LiquidClassID = LiquidClassInfo["Unique Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                RemoveCategoryInstance.LoadSingle(
                    Pipette.BasePipette.LiquidClass(LiquidClassID, LiquidClassVolume)
                )

            AddCategoryInstance = Pipette.BasePipette.LiquidClassCategory(
                UniqueIdentifier + ": Add"
            )
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Add Buffer"]:
                LiquidClassID = LiquidClassInfo["Unique Identifier"]
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

        MagneticRackTrackerInstance.LoadSingle(
            MagneticRack(
                UniqueIdentifier,
                Backend.NullBackend(),
                SupportedLayoutItemTrackerInstance,
            )
        )

    return MagneticRackTrackerInstance
