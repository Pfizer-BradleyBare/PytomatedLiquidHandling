from typing import Generic, TypeVar

from ..Options import OptionsTrackerABC

T = TypeVar("T", bound="OptionsTrackerABC")


class CommandOptionsTracker(Generic[T]):
    def __init__(
        self,
        OptionsTrackerInstance: T,
    ):
        self.OptionsTrackerInstance: T = OptionsTrackerInstance
