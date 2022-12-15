from ..Pipette import TransferOptionsTracker
from .BasePipette import Pipette, PipetteTipTracker, PipettingDeviceTypes


class Pipette8Channel(Pipette):
    def __init__(
        self,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
        ActiveChannels: list[int],
    ):
        Pipette.__init__(
            self,
            PipettingDeviceTypes.Pipette8Channel,
            Enabled,
            SupoortedPipetteTipTrackerInstance,
        )
        self.ActiveChannels: list[int] = ActiveChannels

    def Initialize(self):
        raise NotImplementedError

    def Deinitialize(self):
        raise NotImplementedError

    def Transfer(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError
