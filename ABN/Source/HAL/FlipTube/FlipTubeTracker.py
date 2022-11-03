from .FlipTube import FlipTube
from ...Tools.AbstractClasses import TrackerABC
from ..Labware import LabwareTracker


class FlipTubeTracker(TrackerABC[FlipTube]):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        TrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
