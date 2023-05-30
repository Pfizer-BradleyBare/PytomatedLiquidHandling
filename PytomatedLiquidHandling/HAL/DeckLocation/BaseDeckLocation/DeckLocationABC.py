from ....Tools.AbstractClasses import UniqueObjectABC
from .TransportDeviceConfig import TransportDeviceConfig


class DeckLocationABC(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        TransportDeviceConfigInstance: TransportDeviceConfig,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.TransportDeviceConfigInstance: TransportDeviceConfig = (
            TransportDeviceConfigInstance
        )
