from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportDevices,
)


class InternalPlateGripper(TransportDevice):
    def __init__(
        self,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        TransportDevice.__init__(
            self,
            TransportDevices.InternalPlateGripper,
            TransportableLabwareTrackerInstance,
        )
