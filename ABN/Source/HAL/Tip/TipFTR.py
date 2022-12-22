from typing import Callable

from ...Driver.Tip.FTR import (
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


class TipFTR(Tip):
    def __init__(self, Name: str, PickupSequence: str, MaxVolume: float):
        Tip.__init__(self, Name, PickupSequence, TipTypes.FTR, MaxVolume)

    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        return self.Reload(CallbackFunction, CallbackArgs)

    def Deinitialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        return CommandTracker()

    def Reload(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            LoadTipsCommand(
                "",
                True,
                LoadTipsOptions("", self.PickupSequence),
                CallbackFunction,
                CallbackArgs,
            )
        )

        # We also need to show a deck loading dialog, move the autoload, etc.
        return ReturnCommandTracker

    def UpdateTipPosition(
        self,
        NumTips: int,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

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
                UpdateTipPositionCallback,
                (self, NumTips, CallbackFunction, CallbackArgs),
            )
        )

        return ReturnCommandTracker

    def UpdateRemainingTips(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

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
                (self, CallbackFunction, CallbackArgs),
            )
        )
        return ReturnCommandTracker
