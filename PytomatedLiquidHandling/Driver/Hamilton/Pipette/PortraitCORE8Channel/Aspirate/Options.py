from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


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

    def __init__(
        self,
        *,
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
        Mode: ModeOptions = ModeOptions.Aspiration,
        CapacitiveLiquidLevelDetection: LLDOptions = LLDOptions.Off,
        SubmergeDepth: float = 2,
        PressureLiquidLevelDetection: LLDOptions = LLDOptions.Off,
        MaxHeightDifference: float = 0,
        FixHeightFromBottom: float = 0,
        RetractDistanceForTransportAir: float = 0,
        LiquidFollowing: YesNoOptions = YesNoOptions.No,
        MixCycles: int = 0,
        MixPosition: float = 0,
        MixVolume: float = 0,
    ):
        # Channel Settings
        self.ChannelNumber: int = ChannelNumber

        # Sequence
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.LiquidClass: str = LiquidClass
        self.Volume: float = Volume

        self.Mode: int = Mode.value
        self.CapacitiveLiquidLevelDetection: int = CapacitiveLiquidLevelDetection.value
        self.SubmergeDepth: float = SubmergeDepth
        self.PressureLiquidLevelDetection: int = PressureLiquidLevelDetection.value
        self.MaxHeightDifference: float = MaxHeightDifference
        self.FixHeightFromBottom: float = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float = RetractDistanceForTransportAir

        self.LiquidFollowing: int = LiquidFollowing.value
        self.MixCycles: int = MixCycles
        self.MixPosition: float = MixPosition
        self.MixVolume: float = MixVolume
