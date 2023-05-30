from .....Tools.AbstractClasses import UniqueObjectABC
from ....TransportDevice.BaseTransportDevice import TransportDevice


class TransportDeviceConfig(UniqueObjectABC):
    def __init__(
        self,
        TransportDeviceInstance: TransportDevice,
        HomeGetConfig: dict,
        HomePlaceConfig: dict,
        AwayGetConfig: dict,
        AwayPlaceConfig: dict,
    ):
        UniqueObjectABC.__init__(self, TransportDeviceInstance.GetUniqueIdentifier())
        self.TransportDeviceInstance: TransportDevice = TransportDeviceInstance
        self.HomeGetConfig: dict = HomeGetConfig
        self.HomePlaceConfig: dict = HomePlaceConfig
        self.AwayGetConfig: dict = AwayGetConfig
        self.AwayPlaceConfig: dict = AwayPlaceConfig

        if not all(
            Key in self.HomeGetConfig
            for Key in self.TransportDeviceInstance.GetGetConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Home Get Config. Please fix. Expected: "
                + str(self.TransportDeviceInstance.GetGetConfigKeys())
            )

        if not all(
            Key in self.HomePlaceConfig
            for Key in self.TransportDeviceInstance.GetPlaceConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Home Place Config. Please fix. Expected: "
                + str(self.TransportDeviceInstance.GetPlaceConfigKeys())
            )

        if not all(
            Key in self.AwayGetConfig
            for Key in self.TransportDeviceInstance.GetGetConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Away Get Config. Please fix. Expected: "
                + str(self.TransportDeviceInstance.GetGetConfigKeys())
            )

        if not all(
            Key in self.AwayPlaceConfig
            for Key in self.TransportDeviceInstance.GetPlaceConfigKeys()
        ):
            raise Exception(
                "Keys are missing from Away Place Config. Please fix. Expected: "
                + str(self.TransportDeviceInstance.GetPlaceConfigKeys())
            )
        # Confirm expected keys are in ExtraConfig
