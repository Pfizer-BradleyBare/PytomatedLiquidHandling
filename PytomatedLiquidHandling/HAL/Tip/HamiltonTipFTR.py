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

    def TipCounterEditTime(self) -> float:
        return 0

    def GetTipPositions(self, Options: TipABC.Options) -> list[int]:
        CommandInstance = FTRDriver.GetTipPositions.Command(
            Options=FTRDriver.GetTipPositions.Options(
                TipSequence=self.PickupSequence,
                NumPositions=Options.NumTips,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, FTRDriver.GetTipPositions.Response
        )

        return ResponseInstance.GetTipPositions()

    def GetTipPositionsTime(self, Options: TipABC.Options) -> float:
        return 0

    def GetRemainingTips(self) -> int:
        CommandInstance = FTRDriver.GetNumTips.Command(
            Options=FTRDriver.GetNumTips.Options(
                TipSequence=self.PickupSequence,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, FTRDriver.GetNumTips.Response
        )

        return ResponseInstance.GetNumRemaining()

    def GetRemainingTipsTime(self) -> float:
        return 0
