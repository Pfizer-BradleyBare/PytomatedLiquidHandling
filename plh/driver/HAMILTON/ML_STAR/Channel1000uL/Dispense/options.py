from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class ModeOptions(Enum):
    JetPartVolume = 0
    JetEmptyTip = 1
    SurfacePartVolume = 2
    SurfaceEmptyTip = 3
    DrainTipInJetMode = 4
    FromLiquidClassDefinition = 8
    BlowoutTip = 9


class LLDOptions(Enum):
    Off = 0
    VeryHigh = 1
    High = 2
    Medium = 3
    Low = 4
    FromLabwareDefinition = 5


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    ChannelNumber: int
    LabwareID: str
    PositionID: str
    LiquidClass: str
    Volume: float
    Mode: ModeOptions = ModeOptions.FromLiquidClassDefinition
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    SideTouch: bool = False
    LiquidFollowing: bool = False
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
