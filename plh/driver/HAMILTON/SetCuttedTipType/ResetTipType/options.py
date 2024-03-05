from pydantic import dataclasses

from plh.driver.HAMILTON.complex_inputs import TipTypeOptions
from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    TipType: TipTypeOptions
