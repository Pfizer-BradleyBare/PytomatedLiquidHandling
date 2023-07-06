from dataclasses import dataclass

from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from .DeckLocationTransportConfig import DeckLocationTransportConfig


@dataclass
class DeckLocationTransportConfigTracker(
    UniqueObjectTrackerABC[DeckLocationTransportConfig]
):
    ...
