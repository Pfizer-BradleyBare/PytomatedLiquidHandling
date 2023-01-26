from ...Driver.Tip.NTR import (
    LoadTipsCommand,
    LoadTipsOptions,
    TipsAvailableCommand,
    TipsAvailableOptions,
    TipsRemainingCommand,
    TipsRemainingOptions,
)
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
            LoadTipsCommand(
                "",
                LoadTipsOptions(
                    "",
                    self.PickupSequence,
                    self.NTRWasteSequence,
                    self.GripperSequence,
                ),
                True,
            ).Execute()

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(
        self,
        NumTips: int,
    ):

        try:
            Command = TipsAvailableCommand(
                "",
                TipsAvailableOptions(
                    "",
                    self.PickupSequence,
                    self.NTRWasteSequence,
                    self.GripperSequence,
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
            Command = TipsRemainingCommand(
                "",
                TipsRemainingOptions(
                    "",
                    self.PickupSequence,
                ),
                True,
            )

            Command.Execute()

            self.RemainingTips = Command.GetResponse().GetAdditional()["NumRemaining"]

        except:
            ...
