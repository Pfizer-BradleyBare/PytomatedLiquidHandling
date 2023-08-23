from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T", bound="list")


@dataclass(kw_only=True)
class CommandOptionsListed(Generic[T]):
    ListedOptions: T
