from abc import abstractmethod
from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from .Interface.TransportInterface import TransportInterface
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)


class TransportDevices(Enum):
    COREGripper = "CORE Gripper"
    InternalPlateGripper = "Internal Plate Gripper"
    TrackGripper = "Track Gripper"


class TransportDevice(ObjectABC, TransportInterface):
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

    @abstractmethod
    def GetConfigKeys(self) -> list[str]:
        raise NotImplementedError
