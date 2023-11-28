from pydantic import dataclasses

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    ToolLabwareID: str
