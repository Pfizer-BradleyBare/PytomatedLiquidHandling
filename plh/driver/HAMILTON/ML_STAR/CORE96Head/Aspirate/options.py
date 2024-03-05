from enum import Enum

from pydantic import dataclasses

from plh.driver.tools import OptionsBase


class ModeOptions(Enum):
    Aspiration = 0
    ConsequtiveAspiration = 1
    AspirateAll = 2


class LLDOptions(Enum):
    Off = 0
    VeryHigh = 1
    High = 2
    Medium = 3
    Low = 4
    FromLabwareDefinition = 5


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    LiquidClass: str
    Volume: float
    Mode: ModeOptions = ModeOptions.Aspiration
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    LiquidFollowing: bool = False
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
