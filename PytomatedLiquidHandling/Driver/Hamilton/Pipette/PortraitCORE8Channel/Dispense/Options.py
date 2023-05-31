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

    def __init__(
        self,
        *,
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
        Mode: ModeOptions = ModeOptions.FromLiquidClassDefinition,
        FixHeightFromBottom: float = 0,
        RetractDistanceForTransportAir: float = 0,
        CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off,
        SubmergeDepth: float = 2,
        SideTouch: YesNoOptions = YesNoOptions.No,
        LiquidFollowing: YesNoOptions = YesNoOptions.No,
        MixCycles: int = 0,
        MixPosition: float = 0,
        MixVolume: float = 0,
    ):
        self.ChannelNumber: int = ChannelNumber

        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.Volume: float = Volume

        self.LiquidClass: str = LiquidClass

        self.Mode: int = Mode.value
        self.FixHeightFromBottom: float = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float = RetractDistanceForTransportAir
        self.CapacitiveLiquidLevelDetection: int = CapacitiveLiquidLevelDetection.value
        self.SubmergeDepth: float = SubmergeDepth
        self.SideTouch: int = SideTouch.value

        self.LiquidFollowing: int = LiquidFollowing.value
        self.MixCycles: int = MixCycles
        self.MixPosition: float = MixPosition
        self.MixVolume: float = MixVolume
