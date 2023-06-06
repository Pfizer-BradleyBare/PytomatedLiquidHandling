from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from .BaseDeckLocation import DeckLocationABC
from dataclasses import dataclass


@dataclass
class DeckLocationTracker(UniqueObjectTrackerABC[DeckLocationABC]):
    pass
