from pydantic import dataclasses
from typing import Literal
from enum import Enum


class ColumnNames(Enum):
    ...


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[ColumnNames]):
    Separator: Literal[";"] | Literal[","] | Literal["tab"] = ","
    NoResultValue: str = "N/A"
