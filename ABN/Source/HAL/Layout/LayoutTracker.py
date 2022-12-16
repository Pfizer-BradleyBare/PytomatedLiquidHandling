from ...Tools.AbstractClasses import TrackerABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from .Layout import LayoutItem


class LayoutTracker(TrackerABC[LayoutItem]):
    pass
