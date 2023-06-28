import yaml

from ..Backend import NullBackend
from ..LayoutItem import LayoutItemTracker, Lid
from ..Pipette import PipetteTracker
from ..Pipette.BasePipette import LiquidClass, LiquidClassCategory
from .BaseMagneticRack import MagneticRackTracker
from .MagneticRack import MagneticRack


def LoadYaml(
    FilePath: str,
    LayoutItemTrackerInstance: LayoutItemTracker,
    PipetteTrackerInstance: PipetteTracker,
) -> MagneticRackTracker:
    MagneticRackTrackerInstance = MagneticRackTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Rack in ConfigFile["Rack IDs"]:
        UniqueIdentifier = Rack["Unique Identifier"]

        SupportedLayoutItemTrackerInstance = LayoutItemTracker()

        for LayoutItemUniqueID in Rack[
            "Supported Labware Layout Item Unique Identifiers"
        ]:
            LayoutItemInstance = LayoutItemTrackerInstance.GetObjectByName(
                LayoutItemUniqueID
            )

            if isinstance(LayoutItemInstance, Lid):
                raise Exception(
                    "Only coverable or nonCoverable layout items are supported"
                )

            SupportedLayoutItemTrackerInstance.LoadSingle(LayoutItemInstance)

        for PipetteDevice in Rack["Pipette Unique Identifiers"]:
            PipetteID = PipetteDevice["Unique Identifier"]
            PipetteInstance = PipetteTrackerInstance.GetObjectByName(PipetteID)

            RemoveCategoryInstance = LiquidClassCategory(UniqueIdentifier + ": Remove")
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Remove Buffer"]:
                LiquidClassID = LiquidClassInfo["Unique Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                RemoveCategoryInstance.LoadSingle(
                    LiquidClass(LiquidClassID, LiquidClassVolume)
                )

            AddCategoryInstance = LiquidClassCategory(UniqueIdentifier + ": Add")
            for LiquidClassInfo in PipetteDevice["Liquid Classes"]["Add Buffer"]:
                LiquidClassID = LiquidClassInfo["Unique Identifier"]
                LiquidClassVolume = LiquidClassInfo["Max Volume"]
                AddCategoryInstance.LoadSingle(
                    LiquidClass(LiquidClassID, LiquidClassVolume)
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
                NullBackend(),
                SupportedLayoutItemTrackerInstance,
            )
        )

    return MagneticRackTrackerInstance
