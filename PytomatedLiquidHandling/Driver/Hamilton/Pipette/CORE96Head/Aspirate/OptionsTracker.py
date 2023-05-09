from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC

from .Options import Options


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(
        self,
        *,
        Sequence: str,
        LiquidClass: str,
        Volume: float,
        Mode: int = 0,
        CapacitiveLiquidLevelDetection: int = 0,
        SubmergeDepth: float = 0,
        FixHeightFromBottom: float = 0,
        RetractDistanceForTransportAir: float = 0,
        LiquidFollowing: int = 0,
        MixCycles: int = 0,
        MixPosition: float = 0,
        MixVolume: float = 0,
    ):
        NonUniqueObjectTrackerABC.__init__(self)

        self.Sequence: str = Sequence

        self.Volume: float = Volume

        self.LiquidClass: str = LiquidClass

        self.Mode: int = Mode

        self.CapacitiveLiquidLevelDetection: int = CapacitiveLiquidLevelDetection
        self.SubmergeDepth: float = SubmergeDepth
        self.FixHeightFromBottom: float = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float = RetractDistanceForTransportAir

        self.LiquidFollowing: int = LiquidFollowing
        self.MixCycles: int = MixCycles
        self.MixPosition: float = MixPosition
        self.MixVolume: float = MixVolume
