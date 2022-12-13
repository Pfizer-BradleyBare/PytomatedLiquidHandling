from ...Driver.Tip.FTR import (
    LoadTipsCommand,
    LoadTipsOptions,
    TipsAvailableCommand,
    TipsAvailableOptions,
    TipsRemainingCommand,
    TipsRemainingOptions,
)
from ...Driver.Tools import CommandTracker
from .BaseTip import Tip, TipTypes


class TipFTR(Tip):
    def __init__(self, Name: str, PickupSequence: str, MaxVolume: float):
        Tip.__init__(self, Name, PickupSequence, TipTypes.FTR, MaxVolume)

    def Initialize(self) -> CommandTracker:
        raise NotImplementedError

    def Deinitialize(self) -> CommandTracker:
        raise NotImplementedError

    def Reload(self) -> CommandTracker:
        raise NotImplementedError

    def GetNextAvailableTipPosition(self) -> CommandTracker:
        raise NotImplementedError

    def GetRemainingTips(self) -> CommandTracker:
        raise NotImplementedError
