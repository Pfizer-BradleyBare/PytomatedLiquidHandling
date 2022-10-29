from .FlipTube import FlipTube
from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker


class FlipTubeTracker(TrackerABC[FlipTube]):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        TrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
