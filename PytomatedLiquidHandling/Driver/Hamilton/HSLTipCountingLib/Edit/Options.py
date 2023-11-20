from dataclasses import dataclass, field

from ....Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    LabwareID: str


@dataclass
class ListedOptions(list[Options]):
    TipCounter: str
    DialogTitle: str
    Timeout: int = field(init=True, default=1000)
