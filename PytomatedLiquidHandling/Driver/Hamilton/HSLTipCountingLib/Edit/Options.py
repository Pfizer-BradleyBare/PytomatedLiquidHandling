from pydantic import Field, dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    LabwareID: str


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    TipCounter: str
    DialogTitle: str
    Timeout: int = Field(default=1000)
