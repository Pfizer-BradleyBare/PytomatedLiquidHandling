from ...AbstractClasses import TrackerABC
from .Pipette import PipettingDevice
from ..Tip import TipTracker


class PipetteTracker(TrackerABC[PipettingDevice]):
    def __init__(
        self,
        TipTrackerInstance: TipTracker,
    ):
        TrackerABC.__init__(self)
        self.TipTrackerInstance: TipTracker = TipTrackerInstance
