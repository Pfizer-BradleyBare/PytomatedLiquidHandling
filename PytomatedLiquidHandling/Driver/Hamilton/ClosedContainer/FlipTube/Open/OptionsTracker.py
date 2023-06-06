from .....Tools.AbstractClasses import OptionsTrackerABC
from dataclasses import dataclass
from .Options import Options


@dataclass(kw_only=True)
class OptionsTracker(OptionsTrackerABC[Options]):
    ToolSequence: str
