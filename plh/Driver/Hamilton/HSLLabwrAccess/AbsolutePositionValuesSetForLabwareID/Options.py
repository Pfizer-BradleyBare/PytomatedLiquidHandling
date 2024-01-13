import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    LabwareID: str
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float = 0
