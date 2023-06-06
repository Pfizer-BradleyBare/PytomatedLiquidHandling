from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from . import DeckLocationABC
from dataclasses import dataclass


@dataclass
class DeckLocationTracker(UniqueObjectTrackerABC[DeckLocationABC]):
    pass
