from ..Labware import LabwareTracker
from ..Pipette import TransferOptionsTracker
from .BasePipette import Pipette, PipetteTipTracker, PipettingDeviceTypes


class Pipette96Channel(Pipette):
    def __init__(
        self,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        Pipette.__init__(
            self,
            PipettingDeviceTypes.Pipette96Channel,
            Enabled,
            SupoortedPipetteTipTrackerInstance,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(self):
        ...

    def Deinitialize(self):
        ...

    def Transfer(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        ...
