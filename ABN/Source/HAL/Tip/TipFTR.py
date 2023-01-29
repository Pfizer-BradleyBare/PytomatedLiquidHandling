from ...Driver.Tip import FTR as FTRDriver
from .BaseTip import Tip, TipTypes


class TipFTR(Tip):
    def __init__(self, Name: str, PickupSequence: str, MaxVolume: float):
        Tip.__init__(self, Name, PickupSequence, TipTypes.FTR, MaxVolume)

    def Initialize(
        self,
    ):

        self.Reload()

    def Deinitialize(
        self,
    ):
        ...

    def Reload(
        self,
    ):

        try:
            FTRDriver.LoadTipsCommand(
                "", FTRDriver.LoadTipsOptions("", self.PickupSequence), True
            ).Execute()

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(
        self,
        NumTips: int,
    ):

        try:
            Command = FTRDriver.TipsAvailableCommand(
                "",
                FTRDriver.TipsAvailableOptions(
                    "",
                    self.PickupSequence,
                    NumTips,
                ),
                True,
            )

            Command.Execute()

            self.TipPosition = Command.GetResponse().GetAdditional()["TipPosition"]

        except:
            ...

    def UpdateRemainingTips(
        self,
    ):

        try:
            Command = FTRDriver.TipsRemainingCommand(
                "",
                FTRDriver.TipsRemainingOptions(
                    "",
                    self.PickupSequence,
                ),
                True,
            )

            Command.Execute()

            self.RemainingTips = Command.GetResponse().GetAdditional()["NumRemaining"]

        except:
            ...
