from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedMultiOptionsABC


class AdvancedOptions(AdvancedMultiOptionsABC):
    def __init__(
        self,
        *,
        Mode: int | None = None,
        CapacitiveLiquidLevelDetection: int | None = None,
        SubmergeDepth: float | None = None,
        FixHeightFromBottom: float | None = None,
        RetractDistanceForTransportAir: float | None = None,
        LiquidFollowing: int | None = None,
        MixCycles: int | None = None,
        MixPosition: float | None = None,
        MixVolume: float | None = None,
    ):
        AdvancedMultiOptionsABC.__init__(self)
        self.Mode: int | None = Mode

        self.CapacitiveLiquidLevelDetection: int | None = CapacitiveLiquidLevelDetection
        self.SubmergeDepth: float | None = SubmergeDepth
        self.FixHeightFromBottom: float | None = FixHeightFromBottom
        self.RetractDistanceForTransportAir: float | None = (
            RetractDistanceForTransportAir
        )

        self.LiquidFollowing: int | None = LiquidFollowing
        self.MixCycles: int | None = MixCycles
        self.MixPosition: float | None = MixPosition
        self.MixVolume: float | None = MixVolume


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.Volume: float = Volume

        self.LiquidClass: str = LiquidClass

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            Mode=0,
            CapacitiveLiquidLevelDetection=0,
            SubmergeDepth=2,
            FixHeightFromBottom=0,
            RetractDistanceForTransportAir=0,
            LiquidFollowing=0,
            MixCycles=0,
            MixPosition=0,
            MixVolume=0,
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
