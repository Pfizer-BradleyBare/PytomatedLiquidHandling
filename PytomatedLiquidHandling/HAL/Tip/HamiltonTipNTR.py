from dataclasses import dataclass, field

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import NTR as NTRDriver
from .Base import TipABC


@dataclass
class HamiltonTipNTR(TipABC):
    BackendInstance: HamiltonBackendABC
    NTRWasteSequence: str
    GripperSequence: str
    GeneratedWasteSequence: str = field(init=False, default="")

    def TipCounterEdit(self):
        CommandInstance = NTRDriver.LoadTips.Command(
            Options=NTRDriver.LoadTips.Options(
                TipSequence=self.PickupSequence,
                RackWasteSequence=self.NTRWasteSequence,
                GripperSequence=self.GripperSequence,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, NTRDriver.LoadTips.Response)

    def GetTotalRemainingTips(self) -> int:
        CommandInstance = NTRDriver.GetTotalRemainingTips.Command(
            Options=NTRDriver.GetTotalRemainingTips.Options(
                TipSequence=self.PickupSequence,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, NTRDriver.GetTotalRemainingTips.Response
        )

        return ResponseInstance.GetTotalRemaining()

    def GetRemainingSequencePositions(self) -> list[int]:
        CommandInstance = NTRDriver.GetTotalRemainingTipPositions.Command(
            Options=NTRDriver.GetTotalRemainingTipPositions.Options(
                TipSequence=self.PickupSequence
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )

        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, NTRDriver.GetTotalRemainingTipPositions.Response
        )

        return ResponseInstance.GetPositions()

    def GetNextTipLayer(self):
        CommandInstance = NTRDriver.DiscardCurrentLayer.Command(
            Options=NTRDriver.DiscardCurrentLayer.Options(
                TipSequence=self.PickupSequence,
                GeneratedRackWasteSequence=self.GeneratedWasteSequence,
                GripperSequence=self.GripperSequence,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )

        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, NTRDriver.DiscardCurrentLayer.Response
        )
