from pydantic import dataclasses

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    ChannelNumber: int


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[OptionsABC]):
    LabwareID: str
