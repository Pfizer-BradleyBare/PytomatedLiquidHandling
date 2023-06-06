from dataclasses import dataclass

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    Sequence: str
    ChannelNumber: int
    SequencePosition: int
