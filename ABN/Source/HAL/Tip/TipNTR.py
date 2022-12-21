from ...Driver.Tip.NTR import (
    LoadTipsCommand,
    LoadTipsOptions,
    TipsAvailableCommand,
    TipsAvailableOptions,
    TipsRemainingCommand,
    TipsRemainingOptions,
)
from ...Driver.Tools import Command, CommandTracker
from .BaseTip import Tip, TipTypes
from .BaseTip.Interface import UpdateRemainingTipsCallback, UpdateTipPositionCallback


class TipNTR(Tip):
    def __init__(
        self,
        Name: str,
        PickupSequence: str,
        NTRWasteSequence: str,
        GripperSequence: str,
        MaxVolume: float,
    ):
        Tip.__init__(self, Name, PickupSequence, TipTypes.NTR, MaxVolume)
        self.NTRWasteSequence: str = NTRWasteSequence
        self.GripperSequence: str = GripperSequence

        self.GeneratedWasteSequence: str | None = None

    def Initialize(self) -> CommandTracker:
        return self.Reload()

    def Deinitialize(self) -> CommandTracker:
        return CommandTracker()

    def Reload(self) -> CommandTracker:
        def NTRReloadCallback(CommandInstance: Command, args: tuple):

            TipInstance: TipNTR = args[0]
            ResponseInstance = CommandInstance.GetResponse()

            TipInstance.GeneratedWasteSequence = ResponseInstance.GetAdditional()[
                "GeneratedWasteSequence"
            ]

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            LoadTipsCommand(
                "",
                True,
                LoadTipsOptions(
                    "",
                    self.PickupSequence,
                    self.NTRWasteSequence,
                    self.GripperSequence,
                ),
                NTRReloadCallback,
                (self,),
            )
        )

        # We also need to show a deck loading dialog, move the autoload, etc.
        return ReturnCommandTracker

    def UpdateTipPosition(self, NumTips: int) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            TipsAvailableCommand(
                "",
                True,
                TipsAvailableOptions(
                    "",
                    self.PickupSequence,
                    self.NTRWasteSequence,
                    self.GripperSequence,
                    NumTips,
                ),
                UpdateTipPositionCallback,
                (self, NumTips),
            )
        )

        return ReturnCommandTracker

    def UpdateRemainingTips(self) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            TipsRemainingCommand(
                "",
                True,
                TipsRemainingOptions(
                    "",
                    self.PickupSequence,
                ),
                UpdateRemainingTipsCallback,
                (self,),
            )
        )

        return ReturnCommandTracker
