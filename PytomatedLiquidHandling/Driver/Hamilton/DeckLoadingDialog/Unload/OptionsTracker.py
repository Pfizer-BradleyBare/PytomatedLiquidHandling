from ....Tools.AbstractClasses import OptionsTrackerABC
from .Options import Options

from dataclasses import dataclass


@dataclass(kw_only=True)
class OptionsTracker(OptionsTrackerABC[Options]):
    ToolSequence: str
