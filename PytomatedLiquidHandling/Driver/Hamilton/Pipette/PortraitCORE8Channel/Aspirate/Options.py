from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
        Mode: int = 0,
        CapacitiveLiquidLevelDetection: int = 0,
        SubmergeDepth: float = 0,
        PressureLiquidLevelDetection: int = 0,
        MaxHeightDifference: float = 0,
        FixHeightFromBottom: float = 0,
        RetractDistanceForTransportAir: float = 0,
        LiquidFollowing: int = 0,
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

        self.Mode: int = Mode
        self.CapacitiveLiquidLevelDetection: int = CapacitiveLiquidLevelDetection
        self.SubmergeDepth: float = SubmergeDepth
        self.PressureLiquidLevelDetection: int = PressureLiquidLevelDetection
        self.MaxHeightDifference: float = MaxHeightDifference
        self.FixHeightFromBottom: float = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float = RetractDistanceForTransportAir

        self.LiquidFollowing: int = LiquidFollowing
        self.MixCycles: int = MixCycles
        self.MixPosition: float = MixPosition
        self.MixVolume: float = MixVolume
