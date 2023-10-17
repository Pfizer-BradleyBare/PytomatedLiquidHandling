from dataclasses import dataclass

from .....Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    LabwareID: str
    PositionID: str


@dataclass
class ListedOptions(list[Options]):
    TipCounter: str
