from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class ZModeOptions(Enum):
    MaxHeight = 0
    TraverseHeight = 1
    LabwareClearanceHeight = 2
    ContainerBottom = 3


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    ZMode: ZModeOptions = ZModeOptions.MaxHeight
