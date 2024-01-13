import dataclasses
from typing import Generic, TypeVar

T = TypeVar("T", bound="list")


@dataclasses.dataclass(kw_only=True)
class CommandOptionsListed(Generic[T]):
    """Mixin for command. This gives your command the ability to have a list of options.
    Must be typed with a typed list according to your command options."""

    options: T
    # Have to skip validation due to pydantic error...
    """Typed list of options for your command."""
