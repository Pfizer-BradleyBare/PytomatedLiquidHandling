from ....HAL.Pipette.BasePipette import PipetteTracker
from ....Tools.AbstractClasses import NonUniqueItemTrackerABC
from .TransferOptions import TransferOptions


class TransferOptionsTracker(NonUniqueItemTrackerABC[TransferOptions]):
    def __init__(self, PipetteTrackerInstance: PipetteTracker):
        NonUniqueItemTrackerABC.__init__(self)
        self.PipetteTrackerInstance: PipetteTracker = PipetteTrackerInstance
