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
            FTRDriver.LoadTips.Command(
                "", FTRDriver.LoadTips.Options("", self.PickupSequence), True
            ).Execute()

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(
        self,
        NumTips: int,
    ):

        try:
            Command = FTRDriver.TipsAvailable.Command(
                "",
                FTRDriver.TipsAvailable.Options(
                    "",
                    self.PickupSequence,
                    NumTips,
                ),
                True,
            )

            Command.Execute()

            self.TipPosition = Command.GetTipPosition()

        except:
            ...

    def UpdateRemainingTips(
        self,
    ):

        try:
            Command = FTRDriver.TipsRemaining.Command(
                "",
                FTRDriver.TipsRemaining.Options(
                    "",
                    self.PickupSequence,
                ),
                True,
            )

            Command.Execute()

            self.RemainingTips = Command.GetNumRemaining()

        except:
            ...
