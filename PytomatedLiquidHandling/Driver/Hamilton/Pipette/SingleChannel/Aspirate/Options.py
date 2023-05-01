from enum import Enum

from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsABC


class AdvancedOptions(AdvancedOptionsABC):
    def __init__(
        self,
        *,
        Mode: int | None = None,
        CapacitiveLiquidLevelDetection: int | None = None,
        SubmergeDepth: float | None = None,
        PressureLiquidLevelDetection: int | None = None,
        MaxHeightDifference: float | None = None,
        FixHeightFromBottom: float | None = None,
        RetractDistanceForTransportAir: float | None = None,
        LiquidFollowing: int | None = None,
        MixCycles: int | None = None,
        MixPosition: float | None = None,
        MixVolume: float | None = None,
    ):
        self.Mode: int | None = Mode
        self.CapacitiveLiquidLevelDetection: int | None = CapacitiveLiquidLevelDetection
        self.SubmergeDepth: float | None = SubmergeDepth
        self.PressureLiquidLevelDetection: int | None = PressureLiquidLevelDetection
        self.MaxHeightDifference: float | None = MaxHeightDifference
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
        ChannelNumber: int,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        # Channel Settings
        self.ChannelNumber: int = ChannelNumber

        # Sequence
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        self.LiquidClass: str = LiquidClass
        self.Volume: float = Volume

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            Mode=0,
            CapacitiveLiquidLevelDetection=0,
            SubmergeDepth=0,
            PressureLiquidLevelDetection=0,
            MaxHeightDifference=0,
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
