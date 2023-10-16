from dataclasses import dataclass

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    LabwareID: str
    PositionID: str


@dataclass(kw_only=True)
class ListedOptions(list[Options]):
    ToolSequence: str
