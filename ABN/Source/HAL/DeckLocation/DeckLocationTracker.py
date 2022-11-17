from ...Tools.AbstractClasses import TrackerABC
from ..Transport import TransportTracker
from .DeckLocation import DeckLocation


class DeckLocationTracker(TrackerABC[DeckLocation]):
    def __init__(self, TransportTrackerInstance: TransportTracker):
        TrackerABC.__init__(self)
        self.TransportTrackerInstance: TransportTracker = TransportTrackerInstance
