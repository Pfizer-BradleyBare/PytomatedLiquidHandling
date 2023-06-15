from .....Tools.AbstractClasses import UniqueObjectTrackerABC
from dataclasses import dataclass
from .StepABC import StepABC


@dataclass
class StepTracker(UniqueObjectTrackerABC[StepABC]):
    ...
