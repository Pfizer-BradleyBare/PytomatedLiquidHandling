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
        TransportDevice: TransportDevices,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        UniqueObjectABC.__init__(self, TransportDevice.value)
        self.TransportableLabwareTrackerInstance: TransportableLabwareTracker = (
            TransportableLabwareTrackerInstance
        )

    @abstractmethod
    def GetConfigKeys(self) -> list[str]:
        ...
