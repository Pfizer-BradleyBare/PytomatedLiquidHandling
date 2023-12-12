from typing import Generic, TypeVar

from pydantic import SkipValidation, dataclasses

from ..Options import OptionsABC

T = TypeVar("T", bound="OptionsABC")


@dataclasses.dataclass(kw_only=True)
class CommandOptions(Generic[T]):
    """Mixin for command. This gives your command the ability to have options.
    Must be typed according to your command options."""

    Options: SkipValidation[T]
    """Options for your command."""
