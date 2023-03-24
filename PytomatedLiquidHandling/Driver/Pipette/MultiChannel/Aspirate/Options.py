from enum import Enum

from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(
        self,
        Name: str,
        Sequence: str,
        SequencePosition: int,
        LiquidClass: str,
        Volume: float,
    ):
        self.Name: str = Name

        # Sequence
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

        # Normal Parameters
        self.Volume: float = Volume
        self.Mode: int = 0
        self.LiquidClass: str = LiquidClass
        self.CapacitiveLiquidLevelDetection: int = 0
        self.SubmergeDepth: float = 2
        self.FixHeightFromBottom: float = 0
        self.RetractDistanceForTransportAir: float = 0

        # Advanced
        self.LiquidFollowing: int = 0
        self.MixCycles: int = 0
        self.MixPosition: float = 0
        self.MixVolume: float = 0

    def GetName(self) -> str:
        return self.Name
