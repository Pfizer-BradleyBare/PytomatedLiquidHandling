from enum import Enum

from ......Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
        Mode: int = 0,
        FixHeightFromBottom: float = 0,
        RetractDistanceForTransportAir: float = 0,
        CapacitiveLiquidLevelDetection: int = 0,
        SubmergeDepth: float = 2,
        SideTouch: int = 0,
        LiquidFollowing: int = 0,
        MixCycles: int = 0,
        MixPosition: float = 0,
        MixVolume: float = 0,
    ):
        self.ChannelNumber: int = ChannelNumber

        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.Volume: float = Volume

        self.LiquidClass: str = LiquidClass

        self.Mode: int = Mode
        self.FixHeightFromBottom: float = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float = RetractDistanceForTransportAir
        self.CapacitiveLiquidLevelDetection: int = CapacitiveLiquidLevelDetection
        self.SubmergeDepth: float = SubmergeDepth
        self.SideTouch: int = SideTouch

        self.LiquidFollowing: int = LiquidFollowing
        self.MixCycles: int = MixCycles
        self.MixPosition: float = MixPosition
        self.MixVolume: float = MixVolume
