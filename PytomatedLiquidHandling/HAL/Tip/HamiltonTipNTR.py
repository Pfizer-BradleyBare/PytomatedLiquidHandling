from ...Driver.Hamilton.Tip import NTR as NTRDriver
from .BaseTip import Tip
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from dataclasses import dataclass, field


@dataclass
class HamiltonTipNTR(Tip):
    BackendInstance: HamiltonBackendABC
    NTRWasteSequence: str
    GripperSequence: str
    GeneratedWasteSequence: str = field(init=False, default="")

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
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            self.BackendInstance.GetResponse(
                CommandInstance, NTRDriver.LoadTips.Response
            )

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
                CustomErrorHandling=self.CustomErrorHandling,
            )

            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, NTRDriver.GetTipPositions.Response
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
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, NTRDriver.GetNumTips.Response
            )

            self.RemainingTips = ResponseInstance.GetNumRemaining()

        except:
            ...
