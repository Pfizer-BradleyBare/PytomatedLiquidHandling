from typing import Callable

from ...Driver.NOP import NOPCommand
from ...Driver.Tip.NTR import (
    LoadTipsCommand,
    LoadTipsOptions,
    TipsAvailableCommand,
    TipsAvailableOptions,
    TipsRemainingCommand,
    TipsRemainingOptions,
)
from ...Driver.Tools import Command, CommandTracker, ExecuteCallback
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

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "TipNTR Deinitialize NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Reload(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        def NTRReloadCallback(CommandInstance: Command, args: tuple):

            TipInstance: TipNTR = args[0]
            ResponseInstance = CommandInstance.GetResponse()

            TipInstance.GeneratedWasteSequence = ResponseInstance.GetAdditional()[
                "GeneratedWasteSequence"
            ]

            ExecuteCallback(args[1], CommandInstance, args[2])

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            LoadTipsCommand(
                "",
                LoadTipsOptions(
                    "",
                    self.PickupSequence,
                    self.NTRWasteSequence,
                    self.GripperSequence,
                ),
                None,
                NTRReloadCallback,
                (self, CallbackFunction, CallbackArgs),
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
                TipsAvailableOptions(
                    "",
                    self.PickupSequence,
                    self.NTRWasteSequence,
                    self.GripperSequence,
                    NumTips,
                ),
                None,
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
                TipsRemainingOptions(
                    "",
                    self.PickupSequence,
                ),
                None,
                UpdateRemainingTipsCallback,
                (self, CallbackFunction, CallbackArgs),
            )
        )

        return ReturnCommandTracker
