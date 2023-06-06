from typing import Generic, TypeVar
from dataclasses import dataclass
from ..Options import OptionsABC

T = TypeVar("T", bound="OptionsABC")


@dataclass(kw_only=True)
class CommandOptions(Generic[T]):
    OptionsInstance: T
