import yaml

from .AutoloadCarrier import AutoloadCarrier
from .BaseCarrier import CarrierTracker
from .MoveableCarrier import MoveableCarrier
from .NonMoveableCarrier import NonMoveableCarrier


def LoadYaml(FilePath: str) -> CarrierTracker:
    CarrierTrackerInstance = CarrierTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceID in ConfigFile:
        for Device in ConfigFile[DeviceID]:
            if Device["Enabled"] == False:
                continue

            UniqueID = Device["Unique Identifier"]

            TrackStart = Device["Track Start"]
            TrackEnd = Device["Track End"]
            NumPositions = Device["Num Labware Positions"]
            Filename3D = Device["Image Filename 3D"]
            Filename2D = Device["Image Filename 2D"]

            if DeviceID == "Moveable Carrier":
                CarrierInstance = MoveableCarrier(
                    UniqueID,
                    TrackStart,
                    TrackEnd,
                    NumPositions,
                    Filename3D,
                    Filename2D,
                )
            elif DeviceID == "Non-Moveable Carrier":
                CarrierInstance = NonMoveableCarrier(
                    UniqueID,
                    TrackStart,
                    TrackEnd,
                    NumPositions,
                    Filename3D,
                    Filename2D,
                )
            elif DeviceID == "Autoload Carrier":
                LabwareID = Device["Labware ID"]
                CarrierInstance = AutoloadCarrier(
                    UniqueID,
                    TrackStart,
                    TrackEnd,
                    NumPositions,
                    Filename3D,
                    Filename2D,
                    LabwareID,
                )
            else:
                raise Exception("Carrier Device not recognized")

            CarrierTrackerInstance.LoadSingle(CarrierInstance)
    return CarrierTrackerInstance
