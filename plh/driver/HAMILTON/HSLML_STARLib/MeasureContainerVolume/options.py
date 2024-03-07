from pydantic import dataclasses

from plh.driver.HAMILTON.complex_inputs import LLDOptions
from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ChannelNumber: int
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    PressureLiquidLevelDetection: LLDOptions = LLDOptions.Off
    MaxHeightDifference: float = 0
