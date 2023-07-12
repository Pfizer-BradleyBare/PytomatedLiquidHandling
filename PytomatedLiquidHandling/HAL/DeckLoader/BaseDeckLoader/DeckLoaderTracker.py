from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .DeckLoaderABC import DeckLoaderABC


@dataclass
class DeckLoaderTracker(UniqueObjectTrackerABC[DeckLoaderABC]):
    pass
