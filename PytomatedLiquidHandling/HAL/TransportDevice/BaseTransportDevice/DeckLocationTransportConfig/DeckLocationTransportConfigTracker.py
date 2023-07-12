from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .DeckLocationTransportConfig import DeckLocationTransportConfig


@dataclass
class DeckLocationTransportConfigTracker(
    UniqueObjectTrackerABC[DeckLocationTransportConfig]
):
    ...
