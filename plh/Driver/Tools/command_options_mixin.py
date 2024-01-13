import dataclasses
from typing import Generic, TypeVar

from .options_base import OptionsBase

T = TypeVar("T", bound=OptionsBase)


@dataclasses.dataclass(kw_only=True)
class CommandOptionsMixin(Generic[T]):
    """Mixin for command. This gives your command the ability to have options.
    Must be typed according to your command options."""

    options: T
    """Options for your command."""
