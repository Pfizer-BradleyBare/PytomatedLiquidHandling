from pydantic import dataclasses

from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    PositionID: str
    ChannelNumber: int


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[OptionsBase]):
    LabwareID: str
