from ...Tools.AbstractClasses import TrackerABC
from ..Tip import TipTracker
from .Pipette import PipettingDevice


class PipetteTracker(TrackerABC[PipettingDevice]):
    def __init__(
        self,
        TipTrackerInstance: TipTracker,
    ):
        TrackerABC.__init__(self)
        self.TipTrackerInstance: TipTracker = TipTrackerInstance
