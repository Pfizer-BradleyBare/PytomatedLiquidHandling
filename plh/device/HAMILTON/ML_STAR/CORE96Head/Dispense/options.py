from pydantic import dataclasses

from plh.device.HAMILTON.complex_inputs import DispenseModeOptions, LLDOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    LiquidClass: str
    Volume: float
    Mode: DispenseModeOptions = DispenseModeOptions.FromLiquidClassDefinition
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    SideTouch: int = 0
    LiquidFollowing: bool = False
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
