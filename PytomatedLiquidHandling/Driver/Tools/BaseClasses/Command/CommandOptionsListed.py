from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T", bound="list")


@dataclass(kw_only=True)
class CommandOptionsListed(Generic[T]):
    """Mixin for command. This gives your command the ability to have a list of options.
    Must be typed with a typed list according to your command options."""

    Options: T
    """Typed list of options for your command."""
