from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.BaseClasses import UniqueObjectTrackerABC

from .Method import Method


@dataclass
class MethodTracker(UniqueObjectTrackerABC[Method]):
    ...
