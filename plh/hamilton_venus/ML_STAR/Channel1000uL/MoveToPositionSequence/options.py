from pydantic import dataclasses

from plh.hamilton_venus.complex_inputs import ZModeOptions
from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    ZMode: ZModeOptions = ZModeOptions.MaxHeight
