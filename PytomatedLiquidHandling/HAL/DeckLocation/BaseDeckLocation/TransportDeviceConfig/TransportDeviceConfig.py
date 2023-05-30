from .....Tools.AbstractClasses import UniqueObjectABC
from ....TransportDevice.BaseTransportDevice import TransportDevice


class TransportDeviceConfig(UniqueObjectABC):
    def __init__(
        self,
        TransportDeviceInstance: TransportDevice,
        HomeConfig: dict,
        AwayConfig: dict,
    ):
        UniqueObjectABC.__init__(self, TransportDeviceInstance.GetUniqueIdentifier())
        self.TransportDeviceInstance: TransportDevice = TransportDeviceInstance
        self.HomeConfig: dict = HomeConfig
        self.AwayConfig: dict = AwayConfig

        if not all(
            Key in self.HomeConfig
            for Key in self.TransportDeviceInstance.GetConfigKeys()
        ):
            raise Exception("Keys are missing from Home Config. Please fix.")

        if not all(
            Key in self.AwayConfig
            for Key in self.TransportDeviceInstance.GetConfigKeys()
        ):
            raise Exception("Keys are missing from Away Config. Please fix.")
        # Confirm expected keys are in ExtraConfig
