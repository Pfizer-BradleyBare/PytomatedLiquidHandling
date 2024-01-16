import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float = 0
