from .....Tools.AbstractClasses import UniqueObjectABC, UniqueObjectTrackerABC
from dataclasses import dataclass, field
from typing import TypeVar, Generic
from .ElutionParameters import ElutionParameters
from enum import Enum

T = TypeVar("T", bound="ElutionParameters")
S = TypeVar("S", bound="Enum")


@dataclass
class DesaltingTip(UniqueObjectABC, Generic[T, S]):
    ElutionParametersTrackerInstance: UniqueObjectTrackerABC[T] = field(
        init=False, default=UniqueObjectTrackerABC()
    )
    TipType: S
