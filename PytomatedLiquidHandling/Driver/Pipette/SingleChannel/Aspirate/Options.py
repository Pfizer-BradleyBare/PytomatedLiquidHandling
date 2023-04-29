from enum import Enum

from .....Tools.AbstractClasses import NonUniqueObjectABC


class AdvancedOptions:
    def init(self):

        self.Mode: int = 0
        self.CapacitiveLiquidLevelDetection: int = 0
        self.SubmergeDepth: float = 2
        self.PressureLiquidLevelDetection: int = 0
        self.MaxHeightDifference: float = 0
        self.FixHeightFromBottom: float = 0
        self.RetractDistanceForTransportAir: float = 0

        self.LiquidFollowing: int = 0
        self.MixCycles: int = 0
        self.MixPosition: float = 0
        self.MixVolume: float = 0


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
    ):
        # Channel Settings
        self.ChannelNumber: int = ChannelNumber

        # Sequence
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.LiquidClass: str = LiquidClass
        self.Volume: float = Volume

        self.Advanced: AdvancedOptions = AdvancedOptions()
