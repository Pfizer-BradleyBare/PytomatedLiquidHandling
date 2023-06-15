from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from .Method import MethodABC
from dataclasses import dataclass


@dataclass
class Scheduler(UniqueObjectTrackerABC[MethodABC]):
    ...
