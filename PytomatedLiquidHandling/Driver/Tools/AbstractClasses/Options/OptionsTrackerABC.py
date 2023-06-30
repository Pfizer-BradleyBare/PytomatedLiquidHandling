from dataclasses import dataclass
from typing import TypeVar

from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .OptionsABC import OptionsABC

T = TypeVar("T", bound="OptionsABC")


@dataclass
class OptionsTrackerABC(NonUniqueObjectTrackerABC[T]):
    ...
