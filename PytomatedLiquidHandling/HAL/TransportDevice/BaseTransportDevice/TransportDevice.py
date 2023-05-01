from abc import abstractmethod
from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface.TransportInterface import TransportInterface
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)


class TransportDevices(Enum):
    COREGripper = "CORE Gripper"
    InternalPlateGripper = "Internal Plate Gripper"
    TrackGripper = "Track Gripper"


class TransportDevice(UniqueObjectABC, TransportInterface):
    def __init__(
        self,
        UniqueIdentifier: TransportDevices,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        self.UniqueIdentifier: TransportDevices = UniqueIdentifier
        self.TransportableLabwareTrackerInstance: TransportableLabwareTracker = (
            TransportableLabwareTrackerInstance
        )

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier.value

    @abstractmethod
    def GetConfigKeys(self) -> list[str]:
        ...
