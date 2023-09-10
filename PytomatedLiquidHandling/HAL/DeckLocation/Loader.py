import os

import yaml

from PytomatedLiquidHandling.HAL import Carrier, TransportDevice

from ...Tools.Logger import Logger
from .Base import CarrierConfig, DeckLocationABC, TransportConfig
from .DeckLocation import DeckLocation


def LoadYaml(
    LoggerInstance: Logger,
    Carriers: dict[str, Carrier.Base.CarrierABC],
    TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC],
    FilePath: str,
) -> dict[str, DeckLocationABC]:
    LoggerInstance.info("Loading DeckLocation config yaml file.")

    DeckLocations: dict[str, DeckLocationABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return DeckLocations

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return DeckLocations

    for Location in ConfigFile:
        if Location["Enabled"] == False:
            LoggerInstance.warning(
                "DeckLocation"
                + " with unique ID "
                + Location["Unique Identifier"]
                + " is not enabled so will be skipped."
            )

            continue

        Identifier = Location["Identifier"]

        CarrierID = Location["Carrier"]["Identifier"]
        CarrierPosition = Location["Carrier"]["Position"]

        CarrierInstance = Carriers[CarrierID]
        CarrierConfigInstance = CarrierConfig(CarrierInstance, CarrierPosition)

        TransportDevice = TransportDevices[
            Location["Transport Config"]["Transport Device Identifier"]
        ]
        PickupOptions = Location["Transport Config"]["Pickup Options"]
        DropoffOptions = Location["Transport Config"]["Dropoff Options"]

        DeckLocationInstance = DeckLocation(
            Identifier,
            CarrierConfigInstance,
            TransportConfig(TransportDevice, PickupOptions, DropoffOptions),
        )

        DeckLocations[Identifier] = DeckLocationInstance

    return DeckLocations
