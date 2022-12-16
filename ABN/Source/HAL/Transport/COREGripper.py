from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportDevices,
)


class COREGripper(TransportDevice):
    def __init__(
        self,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
        GripperSequence: str,
    ):
        self.GripperSequence: str = GripperSequence
        TransportDevice.__init__(
            self, TransportDevices.COREGripper, TransportableLabwareTrackerInstance
        )
