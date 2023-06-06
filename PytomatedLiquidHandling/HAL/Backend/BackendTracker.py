from ...Driver.Tools.AbstractClasses import BackendABC
from ...Tools.AbstractClasses import UniqueObjectTrackerABC
from dataclasses import dataclass


@dataclass
class BackendTracker(UniqueObjectTrackerABC[BackendABC]):
    ...
