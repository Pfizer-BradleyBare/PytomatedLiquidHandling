from pydantic import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    TaughtPathName: str
    CollisionControl: bool = True
