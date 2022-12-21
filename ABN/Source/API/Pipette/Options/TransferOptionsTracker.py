from ....HAL.Pipette.BasePipette import PipetteTracker
from ....Tools.AbstractClasses import TrackerABC
from .TransferOptions import TransferOptions


class TransferOptionsTracker(TrackerABC[TransferOptions]):
    def __init__(self, PipetteTrackerInstance: PipetteTracker):
        TrackerABC.__init__(self)
        self.PipetteTrackerInstance: PipetteTracker = PipetteTrackerInstance
