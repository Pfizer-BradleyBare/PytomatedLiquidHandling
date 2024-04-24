import dataclasses
from typing import Generic, Sequence, TypeVar

from .options_base import OptionsBase

T = TypeVar("T", bound="Sequence[OptionsBase]")


@dataclasses.dataclass(kw_only=True)
class CommandOptionsListMixin(Generic[T]):
    """Mixin for command. This gives your command the ability to have a list of options.
    Must be typed with a typed list according to your command options."""

    options: T
    # Have to skip validation due to pydantic error...
    """Typed list of options for your command."""
