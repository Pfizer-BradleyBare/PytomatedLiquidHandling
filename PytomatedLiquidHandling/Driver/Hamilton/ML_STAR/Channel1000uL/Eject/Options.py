from dataclasses import dataclass

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    ChannelNumber: int
    LabwareID: str
    PositionID: str
