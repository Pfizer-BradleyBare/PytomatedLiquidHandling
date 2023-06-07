from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .MagneticRackABC import MagneticRackABC
from dataclasses import dataclass


@dataclass
class MagneticRackTracker(UniqueObjectTrackerABC[MagneticRackABC]):
    ...
