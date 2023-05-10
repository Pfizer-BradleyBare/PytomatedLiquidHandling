from abc import abstractmethod
from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface.TransportInterface import TransportInterface
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)


class TransportDevice(UniqueObjectABC, TransportInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.TransportableLabwareTrackerInstance: TransportableLabwareTracker = (
            TransportableLabwareTrackerInstance
        )
        TransportInterface.__init__(self, CustomErrorHandling)

    @abstractmethod
    def GetConfigKeys(self) -> list[str]:
        ...
