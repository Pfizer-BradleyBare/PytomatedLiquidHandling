from ...Driver.Hamilton.Tip import NTR as NTRDriver
from .BaseTip import Tip
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class HamiltonTipNTR(Tip):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        PickupSequence: str,
        NTRWasteSequence: str,
        GripperSequence: str,
        MaxVolume: float,
    ):
        Tip.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            PickupSequence,
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
            CommandInstance = NTRDriver.LoadTips.Command(
                OptionsInstance=NTRDriver.LoadTips.Options(
                    TipSequence=self.PickupSequence,
                    RackWasteSequence=self.NTRWasteSequence,
                    GripperSequence=self.GripperSequence,
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            self.GetBackend().GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPositions(self, *, NumTips: int):
        try:
            CommandInstance = NTRDriver.GetTipPositions.Command(
                OptionsInstance=NTRDriver.GetTipPositions.Options(
                    TipSequence=self.PickupSequence,
                    GeneratedRackWasteSequence=self.GeneratedWasteSequence,
                    GripperSequence=self.GripperSequence,
                    NumPositions=NumTips,
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )

            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.TipPositions = ResponseInstance.GetTipPositions()

        except:
            ...

    def UpdateRemainingTips(self):
        try:
            CommandInstance = NTRDriver.GetNumTips.Command(
                OptionsInstance=NTRDriver.GetNumTips.Options(
                    TipSequence=self.PickupSequence,
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.RemainingTips = ResponseInstance.GetNumRemaining()

        except:
            ...
