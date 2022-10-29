from ...AbstractClasses import TrackerABC
from .DeckLocation import DeckLocation
from ..Transport import TransportTracker


class DeckLocationTracker(TrackerABC[DeckLocation]):
    def __init__(self, TransportTrackerInstance: TransportTracker):
        TrackerABC.__init__(self)
        self.TransportTrackerInstance: TransportTracker = TransportTrackerInstance
