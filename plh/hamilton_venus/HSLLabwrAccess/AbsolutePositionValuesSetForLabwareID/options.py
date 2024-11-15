from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float = 0
