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

    def _TipCounterEdit(self):
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

    def _TipCounterEditTime(self) -> float:
        return 0

    def _GetTipPositions(
        self, OptionsInstance: Tip.GetTipPositions.Options
    ) -> list[int]:
        CommandInstance = NTRDriver.GetTipPositions.Command(
            OptionsInstance=NTRDriver.GetTipPositions.Options(
                TipSequence=self.PickupSequence,
                GeneratedRackWasteSequence=self.GeneratedWasteSequence,
                GripperSequence=self.GripperSequence,
                NumPositions=OptionsInstance.NumTips,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )

        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, NTRDriver.GetTipPositions.Response
        )

        return ResponseInstance.GetTipPositions()

    def _GetTipPositionsTime(
        self, OptionsInstance: Tip.GetTipPositions.Options
    ) -> float:
        return 0

    def _GetRemainingTips(self) -> int:
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

        return ResponseInstance.GetNumRemaining()

    def _GetRemainingTipsTime(self) -> float:
        return 0
