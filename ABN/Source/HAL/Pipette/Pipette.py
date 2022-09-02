from enum import Enum
from ..Tip import Tip
from ...AbstractClasses import ObjectABC


class LiquidClass:
    def __init__(self, Name: str, MaxVolume: float, LiquidClass: str):
        self.Name: str = Name
        self.MaxVolume: float = MaxVolume
        self.LiquidClass: str = LiquidClass

    def GetName(self) -> str:
        return self.Name

    def GetMaxVolume(self) -> float:
        return self.MaxVolume

    def GetLiquidClass(self) -> str:
        return self.LiquidClass


class PipettingTip:
    def __init__(self, TipObject: Tip, LiquidClasses: list[LiquidClass]):
        self.TipObject: Tip = TipObject
        self.LiquidClasses: list[LiquidClass] = LiquidClasses

    def GetTip(self) -> Tip:
        return self.TipObject

    def GetLiquidClasses(self) -> list[LiquidClass]:
        return self.LiquidClasses


class DeviceTypes(Enum):
    Portrait1mLChannels = "1mL Channels Portrait"
    Core96Head = "96 Core Head"


class PipettingChannels(ObjectABC):
    def __init__(self, DeviceType: DeviceTypes, Enabled: bool):
        self.Enabled: bool = Enabled
        self.DeviceType: DeviceTypes = DeviceType

    def GetName(self) -> str:
        return self.DeviceType.value

    def GetEnabledState(self):
        return self.Enabled

    def GetType(self) -> DeviceTypes:
        return self.DeviceType


class Portrait1mLChannels(PipettingChannels):
    def __init__(self, ActiveChannels: list[int], Enabled: bool):
        self.ActiveChannels: list[int] = ActiveChannels
        PipettingChannels.__init__(self, DeviceTypes.Portrait1mLChannels, Enabled)

    def GetActiveChannels(self):
        return self.ActiveChannels


class Core96HeadChannels(PipettingChannels):
    def __init__(self, Enabled: bool):
        PipettingChannels.__init__(self, DeviceTypes.Core96Head, Enabled)


class PipettingDevice:
    def __init__(
        self,
        PipettingChannel: PipettingChannels,
        PipettingTips: list[PipettingTip],
    ):
        self.PipettingChannel: PipettingChannels = PipettingChannel
        self.PipettingTips: list[PipettingTip] = PipettingTips

    def GetPipettingChannel(self) -> PipettingChannels:
        return self.PipettingChannel

    def GetPipettingTips(self) -> list[PipettingTip]:
        return self.PipettingTips
