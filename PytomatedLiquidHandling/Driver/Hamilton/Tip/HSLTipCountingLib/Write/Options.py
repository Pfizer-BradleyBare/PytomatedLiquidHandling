from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Hamilton import Tools

from .....Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    LabwareID: str
    PositionID: str


@dataclass
class ListedOptions(list[Options]):
    TipCounter: str
