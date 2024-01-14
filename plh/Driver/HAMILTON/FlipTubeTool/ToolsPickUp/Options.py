import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    ChannelNumber: int


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[OptionsBase]):
    LabwareID: str
