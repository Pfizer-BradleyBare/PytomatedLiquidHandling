from enum import Enum

from .....Tools.BaseClasses import OptionsABC


class Options(OptionsABC):
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

    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    ChannelNumber: int
    LabwareID: str
    PositionID: str
    LiquidClass: str
    Volume: float
    Mode: ModeOptions = ModeOptions.Aspiration
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    PressureLiquidLevelDetection: LLDOptions = LLDOptions.Off
    MaxHeightDifference: float = 0
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    LiquidFollowing: YesNoOptions = YesNoOptions.No
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
