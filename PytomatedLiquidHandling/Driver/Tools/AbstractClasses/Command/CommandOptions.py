from typing import Generic, TypeVar

from ..Options import OptionsABC

T = TypeVar("T", bound="OptionsABC")


class CommandOptions(Generic[T]):
    def __init__(
        self,
        OptionsInstance: T,
    ):
        self.OptionsInstance: T = OptionsInstance
