from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from .Interface.TransportInterface import TransportInterface
from .TransportableLabware.TransportableLabwareTracker import (
    TransportableLabwareTracker,
)
from ....Driver.Tools.AbstractClasses import BackendABC


class TransportDevice(UniqueObjectABC, TransportInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: BackendABC,
        CustomErrorHandling: bool,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.TransportableLabwareTrackerInstance: TransportableLabwareTracker = (
            TransportableLabwareTrackerInstance
        )
        TransportInterface.__init__(self, BackendInstance, CustomErrorHandling)

    @abstractmethod
    def GetConfigKeys(self) -> list[str]:
        ...
