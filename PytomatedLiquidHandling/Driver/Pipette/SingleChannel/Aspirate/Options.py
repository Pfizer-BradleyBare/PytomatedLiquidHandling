from enum import Enum

from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
    ):

        # Sequence
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        # Normal Parameters
        self.Volume: float = Volume
        self.Mode: int = 0
        self.LiquidClass: str = LiquidClass
        self.CapacitiveLiquidLevelDetection: int = 0
        self.SubmergeDepth: float = 2
        self.PressureLiquidLevelDetection: int = 0
        self.MaxHeightDifference: float = 0
        self.FixHeightFromBottom: float = 0
        self.RetractDistanceForTransportAir: float = 0

        # Channel Settings
        self.ChannelNumber: int = ChannelNumber

        # Advanced
        self.LiquidFollowing: int = 0
        self.MixCycles: int = 0
        self.MixPosition: float = 0
        self.MixVolume: float = 0
