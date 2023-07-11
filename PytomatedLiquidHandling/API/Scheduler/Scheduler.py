from dataclasses import dataclass

from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from .Method import MethodABC


@dataclass
class Scheduler(UniqueObjectTrackerABC[MethodABC]):
    ...
