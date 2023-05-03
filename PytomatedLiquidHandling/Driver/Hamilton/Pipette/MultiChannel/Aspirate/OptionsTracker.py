from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .....Tools.AbstractOptions import (
    AdvancedMultiOptionsTrackerABC,
    AdvancedOptionsWrapper,
)
from .Options import Options


class AdvancedOptionsTracker(AdvancedMultiOptionsTrackerABC):
    @AdvancedOptionsWrapper
    def __init__(
        self,
        *,
        CustomErrorHandling: bool = False,
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
        AdvancedMultiOptionsTrackerABC.__init__(self, CustomErrorHandling)

        self.Mode: int = Mode

        self.CapacitiveLiquidLevelDetection: int = CapacitiveLiquidLevelDetection
        self.SubmergeDepth: float = SubmergeDepth
        self.FixHeightFromBottom: float = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float = RetractDistanceForTransportAir

        self.LiquidFollowing: int = LiquidFollowing
        self.MixCycles: int = MixCycles
        self.MixPosition: float = MixPosition
        self.MixVolume: float = MixVolume


class OptionsTracker(NonUniqueObjectTrackerABC[Options]):
    def __init__(
        self,
        *,
        Sequence: str,
        LiquidClass: str,
        Volume: float,
        AdvancedOptionsTrackerInstance: AdvancedOptionsTracker = AdvancedOptionsTracker(),
    ):
        NonUniqueObjectTrackerABC.__init__(self)

        self.Sequence: str = Sequence

        self.Volume: float = Volume

        self.LiquidClass: str = LiquidClass

        self.AdvancedOptionsTrackerInstance: AdvancedOptionsTracker = (
            AdvancedOptionsTrackerInstance
        )
