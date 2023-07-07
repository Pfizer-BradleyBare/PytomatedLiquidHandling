from dataclasses import dataclass, field

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import NTR as NTRDriver
from .BaseTip import Tip


@dataclass
class HamiltonTipNTR(Tip):
    BackendInstance: HamiltonBackendABC
    NTRWasteSequence: str
    GripperSequence: str
    GeneratedWasteSequence: str = field(init=False, default="")

    def Initialize(self):
        Tip.Initialize(self)

        self.Reload()

    def Deinitialize(self):
        ...

    def Reload(self):
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
        self.BackendInstance.GetResponse(CommandInstance, NTRDriver.LoadTips.Response)

    # We also need to show a deck loading dialog, move the autoload, etc.

    def GetTipPositions(self, *, NumTips: int) -> list[int]:
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

        return ResponseInstance.GetTipPositions()

    def _UpdateRemainingTips(self):
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

        self._RemainingTips = ResponseInstance.GetNumRemaining()
