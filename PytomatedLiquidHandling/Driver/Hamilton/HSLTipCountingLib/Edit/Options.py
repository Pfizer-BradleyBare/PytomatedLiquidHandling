from ....Tools.BaseClasses import OptionsABC
import dataclasses


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    LabwareID: str


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    TipCounter: str
    DialogTitle: str
    Timeout: int = 1000
