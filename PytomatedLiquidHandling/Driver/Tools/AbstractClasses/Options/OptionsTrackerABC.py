from .....Tools.AbstractClasses import NonUniqueObjectTrackerABC

from dataclasses import dataclass
from typing import TypeVar

from .OptionsABC import OptionsABC

T = TypeVar("T", bound="OptionsABC")


@dataclass
class OptionsTrackerABC(NonUniqueObjectTrackerABC[T]):
    ...
