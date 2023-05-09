from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .BaseTip import Tip


class TipFTR(Tip):
    def __init__(
        self,
        UniqueIdentifier: str,
        CustomErrorHandling: bool,
        PickupSequence: str,
        MaxVolume: float,
    ):
        Tip.__init__(
            self,
            UniqueIdentifier,
            CustomErrorHandling,
            PickupSequence,
            MaxVolume,
        )

    def Initialize(self):
        self.Reload()

    def Deinitialize(self):
        ...

    def Reload(self):
        try:
            FTRDriver.LoadTips.Command(
                OptionsInstance=FTRDriver.LoadTips.Options(
                    TipSequence=self.PickupSequence
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(
        self,
        *,
        NumTips: int,
    ):
        try:
            Command = FTRDriver.TipsAvailable.Command(
                OptionsInstance=FTRDriver.TipsAvailable.Options(
                    TipSequence=self.PickupSequence,
                    NumPositions=NumTips,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.TipPosition = Command.GetTipPosition()

        except:
            ...

    def UpdateRemainingTips(self):
        try:
            Command = FTRDriver.TipsRemaining.Command(
                OptionsInstance=FTRDriver.TipsRemaining.Options(
                    TipSequence=self.PickupSequence,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.RemainingTips = Command.GetNumRemaining()

        except:
            ...
