from dataclasses import dataclass
from typing import Generic, TypeVar

from .OptionsABC import OptionsABC

T = TypeVar("T", bound="OptionsABC")


@dataclass(kw_only=True)
class CommandOptions(Generic[T]):
    Options: T
