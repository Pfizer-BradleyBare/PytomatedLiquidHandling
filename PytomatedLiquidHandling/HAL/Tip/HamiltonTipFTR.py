from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .Base import TipABC


@dataclass
class HamiltonTipFTR(TipABC):
    BackendInstance: HamiltonBackendABC

    def TipCounterEdit(self):
        CommandInstance = FTRDriver.LoadTips.Command(
            Options=FTRDriver.LoadTips.Options(TipSequence=self.PickupSequence),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, FTRDriver.LoadTips.Response)

    def GetTotalRemainingTips(self) -> int:
        CommandInstance = FTRDriver.GetTotalRemainingTips.Command(
            Options=FTRDriver.GetTotalRemainingTips.Options(
                TipSequence=self.PickupSequence,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, FTRDriver.GetTotalRemainingTips.Response
        )

        return ResponseInstance.GetTotalRemaining()

    def GetRemainingSequencePositions(self) -> list[int]:
        CommandInstance = FTRDriver.GetTotalRemainingTipPositions.Command(
            Options=FTRDriver.GetTotalRemainingTipPositions.Options(
                TipSequence=self.PickupSequence,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, FTRDriver.GetTotalRemainingTipPositions.Response
        )

        return ResponseInstance.GetPositions()

    def GetNextTipLayer(self):
        raise Exception("Not supported")
