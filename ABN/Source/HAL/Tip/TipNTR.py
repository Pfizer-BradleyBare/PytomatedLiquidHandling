from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Driver.Tip.NTR import (
    LoadTipsCommand,
    LoadTipsOptions,
    TipsAvailableCommand,
    TipsAvailableOptions,
    TipsRemainingCommand,
    TipsRemainingOptions,
)
from ...Server.Globals.HandlerRegistry import GetDriverHandler
from .BaseTip import Tip, TipTypes


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

    def Initialize(self):
        self.Reload()

    def Deinitialize(self):
        pass

    def Reload(self):
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        CommandInstance = LoadTipsCommand(
            "",
            True,
            LoadTipsOptions(
                "",
                self.PickupSequence,
                self.NTRWasteSequence,
                self.GripperSequence,
            ),
        )

        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        self.GeneratedWasteSequence = CommandInstance.GetResponse().GetAdditional()[
            "GeneratedWasteSequence"
        ]

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(self, NumTips: int):
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        CommandInstance = TipsAvailableCommand(
            "",
            True,
            TipsAvailableOptions(
                "",
                self.PickupSequence,
                self.NTRWasteSequence,
                self.GripperSequence,
                NumTips,
            ),
        )

        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        Response = CommandInstance.GetResponse()

        self.TipPosition = Response.GetAdditional()["TipPosition"]

        if Response.GetState() == False:
            self.Reload()

            self.UpdateTipPosition(NumTips)

    def GetRemainingTips(self) -> int:
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        CommandInstance = TipsRemainingCommand(
            "",
            True,
            TipsRemainingOptions(
                "",
                self.PickupSequence,
            ),
        )

        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        return CommandInstance.GetResponse().GetAdditional()["NumRemaining"]
