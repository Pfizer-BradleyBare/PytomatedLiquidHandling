import yaml
from .MagneticRack import MagneticRack
from .BaseMagneticRack import MagneticRackTracker
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..TransportDevice import TransportDeviceTracker
from ..Pipette import PipetteTracker
from ..Pipette.BasePipette import LiquidClass, LiquidClassCategory
from ..LayoutItem import NonCoverablePosition, LayoutItemTracker
from ..Backend import NullBackend


def LoadYaml(
    FilePath: str,
    DeckLocationTrackerInstance: DeckLocationTracker,
    LabwareTrackerInstance: LabwareTracker,
    TransportDeviceTrackerInstance: TransportDeviceTracker,
    PipetteTrackerInstance: PipetteTracker,
) -> MagneticRackTracker:
    MagneticRackTrackerInstance = MagneticRackTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Rack in ConfigFile["Rack IDs"]:
        UniqueIdentifier = Rack["Unique Identifier"]
        DeckLocationID = Rack["Deck Location Unique Identifier"]
        DeckLocationInstance = DeckLocationTrackerInstance.GetObjectByName(
            DeckLocationID
        )

        SupportedLayoutItemTrackerInstance = LayoutItemTracker()
        for LayoutItemInfo in Rack["Supported Labware Information"]:
            Sequence = LayoutItemInfo["Plate Sequence"]
            LabwareID = LayoutItemInfo["Plate Labware Unique Identifier"]
            LabwareInstance = LabwareTrackerInstance.GetObjectByName(LabwareID)

            SupportedLayoutItemTrackerInstance.LoadSingle(
                NonCoverablePosition(
                    UniqueIdentifier + " " + Sequence,
                    Sequence,
                    DeckLocationInstance,
                    LabwareInstance,
                )
            )

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
                TransportDeviceTrackerInstance,
                PipetteTrackerInstance,
            )
        )

    return MagneticRackTrackerInstance
