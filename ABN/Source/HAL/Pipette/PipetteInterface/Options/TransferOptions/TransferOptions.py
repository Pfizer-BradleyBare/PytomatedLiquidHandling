from enum import Enum

from ......Tools.AbstractClasses import ObjectABC, OnOff


class TransferOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        SourceSequence: str,
        SourceWell: int,
        SourceLiquidClass: str,
        DestinationSequence: str,
        DestinationWell: int,
        DestinationLiquidClass: str,
        Volume: float,
    ):
        self.Name: str = Name

        self.SourceSequence: str = SourceSequence
        self.SourceWell: int = SourceWell
        self.SourceLiquidClass: str = SourceLiquidClass
        self.SourceMixingCycles: int = 0
        self.SourceCapacitiveLiquidLevelDetection: OnOff = OnOff.Off
        self.SourcePressureLiquidLevelDetection: OnOff = OnOff.Off
        self.SourceLiquidFollowing: OnOff = OnOff.Off
        self.SourceFixedHeight: float = 0

        self.DestinationSequence: str = DestinationSequence
        self.DestinationWell: int = DestinationWell
        self.DestinationLiquidClass: str = DestinationLiquidClass
        self.DestinationMixingCycles: int = 0
        self.DestinationCapacitiveLiquidLevelDetection: OnOff = OnOff.Off
        self.DestinationPressureLiquidLevelDetection: OnOff = OnOff.Off
        self.DestinationLiquidFollowing: OnOff = OnOff.Off
        self.DestinationFixedHeight: float = 0

        self.Volume: float = Volume

    def GetName(self) -> str:
        return self.Name
