from ......Driver.Tools.AbstractClasses import OptionsTrackerABC
from .Options import Options
from dataclasses import dataclass


@dataclass
class OptionsTracker(OptionsTrackerABC[Options]):
    ...
