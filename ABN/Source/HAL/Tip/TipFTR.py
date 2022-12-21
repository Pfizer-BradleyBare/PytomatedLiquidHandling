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
        return self.Reload()

    def Deinitialize(self) -> CommandTracker:
        return CommandTracker()

    def Reload(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            LoadTipsCommand(
                "",
                True,
                LoadTipsOptions(
                    "",
                    self.PickupSequence,
                ),
            )
        )

        # We also need to show a deck loading dialog, move the autoload, etc.
        return ReturnCommandTracker

    def UpdateTipPosition(self, NumTips: int) -> CommandTracker:
        def UpdateTipPositionCallback(args: tuple):
            pass

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            TipsAvailableCommand(
                "",
                True,
                TipsAvailableOptions(
                    "",
                    self.PickupSequence,
                    NumTips,
                ),
            )
        )
        self.TipPosition = CommandInstance.GetResponse().GetAdditional()["TipPosition"]

        return ReturnCommandTracker

    def UpdateRemainingTips(self) -> CommandTracker:
        def UpdateRemainingTipsCallback(args: tuple):
            pass

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            TipsRemainingCommand(
                "",
                True,
                TipsRemainingOptions(
                    "",
                    self.PickupSequence,
                ),
            )
        )
        self.RemainingTips = CommandInstance.GetResponse().GetAdditional()[
            "NumRemaining"
        ]
        return ReturnCommandTracker
