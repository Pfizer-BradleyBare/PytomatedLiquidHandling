from ...Tools.AbstractClasses import TrackerABC
from ..Labware import LabwareTracker
from .Transport import TransportDevice


class TransportTracker(TrackerABC[TransportDevice]):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        TrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
