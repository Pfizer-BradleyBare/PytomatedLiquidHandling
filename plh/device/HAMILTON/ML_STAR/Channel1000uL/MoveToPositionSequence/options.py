from pydantic import dataclasses

from plh.device.HAMILTON.complex_inputs import ZModeOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    ZMode: ZModeOptions = ZModeOptions.MaxHeight
