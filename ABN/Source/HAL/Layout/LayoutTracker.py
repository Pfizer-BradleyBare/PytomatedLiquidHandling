from ...AbstractClasses import TrackerABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .Layout import LayoutItem


class LayoutTracker(TrackerABC[LayoutItem]):
    def __init__(
        self,
        DeckLocationTrackerInstance: DeckLocationTracker,
        LabwareTrackerInstance: LabwareTracker,
    ):
        TrackerABC.__init__(self)
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )
