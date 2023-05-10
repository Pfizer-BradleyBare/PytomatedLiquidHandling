from .....Tools.AbstractClasses import UniqueObjectABC
from ....TransportDevice.BaseTransportDevice import TransportDevice


class TransportDeviceConfig(UniqueObjectABC):
    def __init__(self, TransportDeviceInstance: TransportDevice, ExtraConfig: dict):
        UniqueObjectABC.__init__(self, TransportDeviceInstance.GetUniqueIdentifier())
        self.TransportDeviceInstance: TransportDevice = TransportDeviceInstance
        self.ExtraConfig: dict = ExtraConfig

        if not all(
            Key in self.ExtraConfig
            for Key in self.TransportDeviceInstance.GetConfigKeys()
        ):
            raise Exception("Keys are missing from device config. Please fix.")
        # Confirm expected keys are in ExtraConfig
