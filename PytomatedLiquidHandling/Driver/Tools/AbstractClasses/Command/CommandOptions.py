from typing import Generic, TypeVar

from .....Tools.AbstractClasses import NonUniqueObjectABC

T = TypeVar("T", bound="NonUniqueObjectABC")


class CommandOptions(Generic[T]):
    def __init__(
        self,
        OptionsInstance: T,
    ):
        self.OptionsInstance: T = OptionsInstance
