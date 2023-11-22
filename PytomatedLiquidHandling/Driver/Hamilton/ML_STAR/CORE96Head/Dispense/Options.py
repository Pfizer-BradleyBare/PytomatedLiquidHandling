from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
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

    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    LabwareID: str
    LiquidClass: str
    Volume: float
    Mode: ModeOptions = ModeOptions.FromLiquidClassDefinition
    FixHeightFromBottom: float = 0
    RetractDistanceForTransportAir: float = 0
    CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off
    SubmergeDepth: float = 2
    SideTouch: int = 0
    LiquidFollowing: YesNoOptions = YesNoOptions.No
    MixCycles: int = 0
    MixPosition: float = 0
    MixVolume: float = 0
