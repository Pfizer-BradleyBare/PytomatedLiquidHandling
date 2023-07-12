from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from . import DeckLocationABC


@dataclass
class DeckLocationTracker(UniqueObjectTrackerABC[DeckLocationABC]):
    pass
