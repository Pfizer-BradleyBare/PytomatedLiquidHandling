import logging
import os

import yaml

from .AutoloadCarrier import AutoloadCarrier
from .Base import CarrierABC
from .MoveableCarrier import MoveableCarrier
from .NonMoveableCarrier import NonMoveableCarrier

Logger = logging.getLogger(__name__)


def Load(FilePath: str) -> dict[str, CarrierABC]:
    Logger.info("Loading Carrier config yaml file.")

    Carriers: dict[str, CarrierABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return Carriers

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Carriers

    for DeviceID in ConfigFile:
        for Device in ConfigFile[DeviceID]:
            if Device["Enabled"] == False:
                Logger.warning(
                    DeviceID
                    + " with unique ID "
                    + Device["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = Device["Identifier"]

            TrackStart = Device["Track Start"]
            TrackEnd = Device["Track End"]
            NumPositions = Device["Num Labware Positions"]
            Filename3D = Device["Image Filename 3D"]
            Filename2D = Device["Image Filename 2D"]

            if DeviceID == "Moveable Carrier":
                CarrierInstance = MoveableCarrier(
                    Identifier,
                    TrackStart,
                    TrackEnd,
                    NumPositions,
                    Filename3D,
                    Filename2D,
                )
            elif DeviceID == "Non-Moveable Carrier":
                CarrierInstance = NonMoveableCarrier(
                    Identifier,
                    TrackStart,
                    TrackEnd,
                    NumPositions,
                    Filename3D,
                    Filename2D,
                )
            elif DeviceID == "Autoload Carrier":
                LabwareID = Device["Labware ID"]
                CarrierInstance = AutoloadCarrier(
                    Identifier,
                    TrackStart,
                    TrackEnd,
                    NumPositions,
                    Filename3D,
                    Filename2D,
                    LabwareID,
                )
            else:
                raise Exception("Carrier Device not recognized")

            Carriers[Identifier] = CarrierInstance

    return Carriers
