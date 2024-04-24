from pydantic import dataclasses

from plh.device.HAMILTON.complex_inputs import AspirateModeOptions, LLDOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ChannelNumber: int
    LabwareID: str
    PositionID: str
    LiquidClass: str
    Volume: float
    Mode: AspirateModeOptions = AspirateModeOptions.Aspiration
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    PressureLiquidLevelDetection: LLDOptions = LLDOptions.Off
    MaxHeightDifference: float = 0
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    LiquidFollowing: bool = False
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
