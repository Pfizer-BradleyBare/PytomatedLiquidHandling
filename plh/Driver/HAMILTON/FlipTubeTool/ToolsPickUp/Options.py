import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    ChannelNumber: int


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[OptionsABC]):
    LabwareID: str
