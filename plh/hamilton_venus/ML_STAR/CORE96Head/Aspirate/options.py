from pydantic import dataclasses

from plh.hamilton_venus.complex_inputs import AspirateModeOptions, LLDOptions
from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    LiquidClass: str
    Volume: float
    Mode: AspirateModeOptions = AspirateModeOptions.Aspiration
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    LiquidFollowing: bool = False
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
