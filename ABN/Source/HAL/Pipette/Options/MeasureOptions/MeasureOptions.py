from enum import Enum

from .....Tools.AbstractClasses import ObjectABC, OnOff


class MeasureOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        ChannelNumber: int,
        Sequence: str,
        Well: int,
    ):
        self.Name: str = Name

        self.ChannelNumber: int = ChannelNumber

        self.Sequence: str = Sequence
        self.Well: int = Well
        self.CapacitiveLiquidLevelDetection: OnOff = OnOff.Off
        self.PressureLiquidLevelDetection: OnOff = OnOff.Off

    def GetName(self) -> str:
        return self.Name
