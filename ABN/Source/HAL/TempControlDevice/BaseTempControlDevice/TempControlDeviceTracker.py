from ....Tools.AbstractClasses import TrackerABC
from ...DeckLocation import DeckLocationTracker
from ...Labware import LabwareTracker
from .TempControlDevice import TempControlDevice


class TempControlDeviceTracker(TrackerABC[TempControlDevice]):
    pass
