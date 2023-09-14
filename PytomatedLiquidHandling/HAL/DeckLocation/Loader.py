import os

import yaml

from PytomatedLiquidHandling.HAL import Carrier, TransportDevice

import logging
from .Base import CarrierConfig, DeckLocationABC, TransportConfig
from .DeckLocation import DeckLocation


Logger = logging.getLogger(__name__)


def LoadYaml(
    Carriers: dict[str, Carrier.Base.CarrierABC],
    TransportDevices: dict[str, TransportDevice.Base.TransportDeviceABC],
    FilePath: str,
) -> dict[str, DeckLocationABC]:
    Logger.info("Loading DeckLocation config yaml file.")

    DeckLocations: dict[str, DeckLocationABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return DeckLocations

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return DeckLocations

    for Location in ConfigFile:
        if Location["Enabled"] == False:
            Logger.warning(
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
        PickupOptions = TransportDevice.PickupOptions(
            Location["Transport Config"]["Pickup Options"]
        )
        DropoffOptions = TransportDevice.DropoffOptions(
            Location["Transport Config"]["Dropoff Options"]
        )

        DeckLocationInstance = DeckLocation(
            Identifier,
            CarrierConfigInstance,
            TransportConfig(TransportDevice, PickupOptions, DropoffOptions),
        )

        DeckLocations[Identifier] = DeckLocationInstance

    return DeckLocations
