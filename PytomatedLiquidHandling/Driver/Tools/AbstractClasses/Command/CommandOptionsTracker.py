from typing import Generic, TypeVar
from dataclasses import dataclass
from ..Options import OptionsTrackerABC

T = TypeVar("T", bound="OptionsTrackerABC")


@dataclass(kw_only=True)
class CommandOptionsTracker(Generic[T]):
    OptionsTrackerInstance: T
