import yaml

from PytomatedLiquidHandling.HAL import Carrier

from .BaseDeckLocation import CarrierConfig, DeckLocationTracker
from .DeckLocation import DeckLocation


def LoadYaml(
    CarrierTrackerInstance: Carrier.CarrierTracker,
    FilePath: str,
) -> DeckLocationTracker:
    DeckLocationTrackerInstance = DeckLocationTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Location in ConfigFile:
        if Location["Enabled"] == False:
            continue

        UniqueIdentifier = Location["Unique Identifier"]

        CarrierUniqueID = Location["Carrier"]["Unique Identifier"]
        CarrierPosition = Location["Carrier"]["Position"]

        CarrierInstance = CarrierTrackerInstance.GetObjectByName(CarrierUniqueID)
        CarrierConfigInstance = CarrierConfig(CarrierInstance, CarrierPosition)

        DeckLocationInstance = DeckLocation(UniqueIdentifier, CarrierConfigInstance)

        DeckLocationTrackerInstance.LoadSingle(DeckLocationInstance)

    return DeckLocationTrackerInstance
