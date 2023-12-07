from dataclasses import dataclass
from typing import Generic, TypeVar

from ..Options import OptionsABC

T = TypeVar("T", bound="OptionsABC")


@dataclass(kw_only=True)
class CommandOptions(Generic[T]):
    """Mixin for command. This gives your command the ability to have options.
    Must be typed according to your command options."""

    Options: T
    """Options for your command."""
