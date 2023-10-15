from .....Tools.AbstractClasses import OptionsABC

from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(OptionsABC):
    Sequence: str
    Position: int


@dataclass(kw_only=True)
class ListedOptions(list[Options]):
    ToolSequence: str
