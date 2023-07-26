from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .BaseTip import Tip


@dataclass
class HamiltonTipFTR(Tip):
    BackendInstance: HamiltonBackendABC

    def _TipCounterEdit(self):
        CommandInstance = FTRDriver.LoadTips.Command(
            OptionsInstance=FTRDriver.LoadTips.Options(TipSequence=self.PickupSequence),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, FTRDriver.LoadTips.Response)

    def _TipCounterEditTime(self) -> float:
        return 0

    def _GetTipPositions(
        self, OptionsInstance: Tip.GetTipPositionsInterfaceCommand.Options
    ) -> list[int]:
        CommandInstance = FTRDriver.GetTipPositions.Command(
            OptionsInstance=FTRDriver.GetTipPositions.Options(
                TipSequence=self.PickupSequence,
                NumPositions=OptionsInstance.NumTips,
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
        self, OptionsInstance: Tip.GetTipPositionsInterfaceCommand.Options
    ) -> float:
        return 0

    def _GetRemainingTips(self) -> int:
        CommandInstance = FTRDriver.GetNumTips.Command(
            OptionsInstance=FTRDriver.GetNumTips.Options(
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
