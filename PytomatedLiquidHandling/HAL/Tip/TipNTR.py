from ...Driver.Hamilton.Tip import NTR as NTRDriver
from .BaseTip import Tip, TipTypes


class TipNTR(Tip):
    def __init__(
        self,
        UniqueIdentifier: str,
        CustomErrorHandling: bool,
        PickupSequence: str,
        NTRWasteSequence: str,
        GripperSequence: str,
        MaxVolume: float,
    ):
        Tip.__init__(
            self,
            UniqueIdentifier,
            CustomErrorHandling,
            PickupSequence,
            TipTypes.NTR,
            MaxVolume,
        )
        self.NTRWasteSequence: str = NTRWasteSequence
        self.GripperSequence: str = GripperSequence

        self.GeneratedWasteSequence: str

    def Initialize(self):
        self.Reload()

    def Deinitialize(self):
        ...

    def Reload(self):
        try:
            NTRDriver.LoadTips.Command(
                OptionsInstance=NTRDriver.LoadTips.Options(
                    TipSequence=self.PickupSequence,
                    RackWasteSequence=self.NTRWasteSequence,
                    GripperSequence=self.GripperSequence,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPosition(self, *, NumTips: int):
        try:
            Command = NTRDriver.TipsAvailable.Command(
                OptionsInstance=NTRDriver.TipsAvailable.Options(
                    TipSequence=self.PickupSequence,
                    GeneratedRackWasteSequence=self.GeneratedWasteSequence,
                    GripperSequence=self.GripperSequence,
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
            Command = NTRDriver.TipsRemaining.Command(
                OptionsInstance=NTRDriver.TipsRemaining.Options(
                    TipSequence=self.PickupSequence,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.RemainingTips = Command.GetNumRemaining()

        except:
            ...
