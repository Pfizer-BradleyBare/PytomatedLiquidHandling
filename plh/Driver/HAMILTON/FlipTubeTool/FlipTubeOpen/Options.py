import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str
    PositionID: str
    ChannelNumber: int