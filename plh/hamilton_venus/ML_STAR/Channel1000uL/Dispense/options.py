from pydantic import dataclasses

from plh.hamilton_venus.complex_inputs import DispenseModeOptions, LLDOptions
from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ChannelNumber: int
    LabwareID: str
    PositionID: str
    LiquidClass: str
    Volume: float
    Mode: DispenseModeOptions = DispenseModeOptions.FromLiquidClassDefinition
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    SideTouch: bool = False
    LiquidFollowing: bool = False
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
