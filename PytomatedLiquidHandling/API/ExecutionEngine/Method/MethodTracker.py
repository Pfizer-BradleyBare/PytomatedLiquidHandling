from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectTrackerABC

from .Method import Method


@dataclass
class MethodTracker(UniqueObjectTrackerABC[Method]):
    ...
