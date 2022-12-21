from typing import cast

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Driver.Tip.FTR import (
    LoadTipsCommand,
    LoadTipsOptions,
    TipsAvailableCommand,
    TipsAvailableOptions,
    TipsRemainingCommand,
    TipsRemainingOptions,
)
from ...Server.Globals.HandlerRegistry import GetDriverHandler
from .BaseTip import Tip, TipTypes


class TipFTR(Tip):
    def __init__(self, Name: str, PickupSequence: str, MaxVolume: float):
        Tip.__init__(self, Name, PickupSequence, TipTypes.FTR, MaxVolume)

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
            ),
        )

        __DriverHandlerInstance.ExecuteCommand(CommandInstance)

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(self, NumTips: int):
        __DriverHandlerInstance: DriverHandler = cast(DriverHandler, GetDriverHandler())

        CommandInstance = TipsAvailableCommand(
            "",
            True,
            TipsAvailableOptions(
                "",
                self.PickupSequence,
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
