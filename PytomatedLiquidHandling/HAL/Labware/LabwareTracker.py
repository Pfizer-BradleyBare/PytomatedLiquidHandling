from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from .BaseLabware import LabwareABC
from dataclasses import dataclass


@dataclass
class LabwareTracker(UniqueObjectTrackerABC[LabwareABC]):
    pass
