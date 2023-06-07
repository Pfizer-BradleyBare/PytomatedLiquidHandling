import yaml
from .MagneticRack import MagneticRack
from .BaseMagneticRack import MagneticRackTracker
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..TransportDevice import TransportDeviceTracker
from ..Pipette import PipetteTracker
from ..LayoutItem import NonCoverablePosition, LayoutItemTracker


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

        MagneticRackTrackerInstance.LoadSingle(
            MagneticRack(
                UniqueIdentifier,
                SupportedLayoutItemTrackerInstance,
                TransportDeviceTrackerInstance,
                PipetteTrackerInstance,
            )
        )

    return MagneticRackTrackerInstance
