from typing import Generic, TypeVar

from .....Tools.AbstractClasses import NonUniqueObjectTrackerABC

T = TypeVar("T", bound="NonUniqueObjectTrackerABC")


class CommandOptionsTracker(Generic[T]):
    def __init__(
        self,
        OptionsTrackerInstance: T,
    ):
        self.OptionsTrackerInstance: T = OptionsTrackerInstance
