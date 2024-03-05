from pydantic import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    CollisionControl: bool = True
