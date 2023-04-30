from enum import Enum

from .....Tools.AbstractClasses import NonUniqueObjectABC


class AdvancedOptions:
    def __init__(self):
        self.Mode: int = 0
        self.FixHeightFromBottom: float = 0
        self.RetractDistanceForTransportAir: float = 0
        self.CapacitiveLiquidLevelDetection: int = 0
        self.SubmergeDepth: float = 2
        self.SideTouch: int = 0

        self.LiquidFollowing: int = 0
        self.MixCycles: int = 0
        self.MixPosition: float = 0
        self.MixVolume: float = 0


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
    ):

        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.Volume: float = Volume

        self.LiquidClass: str = LiquidClass

        self.Advanced: AdvancedOptions = AdvancedOptions()
