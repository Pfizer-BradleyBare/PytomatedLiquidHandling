import os

import yaml

from PytomatedLiquidHandling.HAL import Carrier

from ...Tools.Logger import Logger
from .BaseDeckLocation import CarrierConfig, DeckLocationTracker
from .DeckLocation import DeckLocation


def LoadYaml(
    LoggerInstance: Logger,
    CarrierTrackerInstance: Carrier.CarrierTracker,
    FilePath: str,
) -> DeckLocationTracker:
    DeckLocationTrackerInstance = DeckLocationTracker()

    if not os.path.exists(FilePath):
        return DeckLocationTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        return DeckLocationTrackerInstance

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
