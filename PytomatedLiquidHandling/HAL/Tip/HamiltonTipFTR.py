from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .Base import TipABC


@dataclass
class HamiltonTipFTR(TipABC):
    BackendInstance: HamiltonBackendABC

    def _TipCounterEdit(self):
        CommandInstance = FTRDriver.LoadTips.Command(
            Options=FTRDriver.LoadTips.Options(TipSequence=self.PickupSequence),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, FTRDriver.LoadTips.Response)

    def _TipCounterEditTime(self) -> float:
        return 0

    def _GetTipPositions(
        self, Options: TipABC.GetTipPositionsInterfaceCommand.Options
    ) -> list[int]:
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

    def _GetTipPositionsTime(
        self, Options: TipABC.GetTipPositionsInterfaceCommand.Options
    ) -> float:
        return 0

    def _GetRemainingTips(self) -> int:
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

    def _GetRemainingTipsTime(self) -> float:
        return 0
