from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T", bound="list")


@dataclass(kw_only=True)
class CommandOptionsListed(Generic[T]):
    Options: T
