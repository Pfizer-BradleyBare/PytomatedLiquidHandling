from pydantic import Field, dataclasses

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    TipCounter: str
    DialogTitle: str
    Timeout: int = Field(default=1000)
