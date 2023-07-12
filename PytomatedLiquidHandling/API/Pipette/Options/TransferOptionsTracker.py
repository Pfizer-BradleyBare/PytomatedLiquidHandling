from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectTrackerABC

from ....HAL.Pipette.BasePipette import PipetteTracker
from .TransferOptions import TransferOptions


class TransferOptionsTracker(NonUniqueObjectTrackerABC[TransferOptions]):
    def __init__(self, PipetteTrackerInstance: PipetteTracker):
        NonUniqueObjectTrackerABC.__init__(self)
        self.PipetteTrackerInstance: PipetteTracker = PipetteTrackerInstance
