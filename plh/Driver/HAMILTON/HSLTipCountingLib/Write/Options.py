import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    TipCounter: str
