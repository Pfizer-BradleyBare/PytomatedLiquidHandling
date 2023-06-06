from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .TransferOptions import Options
from dataclasses import dataclass


@dataclass
class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    ...
