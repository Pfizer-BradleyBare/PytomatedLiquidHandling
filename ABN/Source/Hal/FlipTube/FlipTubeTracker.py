from ...Tools.AbstractClasses import TrackerABC
from ..Labware import LabwareTracker
from .FlipTube import FlipTube


class FlipTubeTracker(TrackerABC[FlipTube]):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        TrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
