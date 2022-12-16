from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)


class TransportDevices(Enum):
    COREGripper = "CORE Gripper"
    InternalPlateGripper = "Internal Plate Gripper"
    TrackGripper = "Track Gripper"


class TransportDevice(ObjectABC):
    def __init__(
        self,
        Name: TransportDevices,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        self.Name: TransportDevices = Name
        self.TransportableLabwareTrackerInstance: TransportableLabwareTracker = (
            TransportableLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name.value
