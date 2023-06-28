from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .BaseTip import Tip


@dataclass
class HamiltonTipFTR(Tip):
    BackendInstance: HamiltonBackendABC

    def Initialize(self):
        self.Reload()

    def Deinitialize(self):
        ...

    def Reload(self):
        CommandInstance = FTRDriver.LoadTips.Command(
            OptionsInstance=FTRDriver.LoadTips.Options(TipSequence=self.PickupSequence),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        self.BackendInstance.GetResponse(CommandInstance, FTRDriver.LoadTips.Response)

    # We also need to show a deck loading dialog, move the autoload, etc.

    def GetTipPositions(self, *, NumTips: int) -> list[int]:
        CommandInstance = FTRDriver.GetTipPositions.Command(
            OptionsInstance=FTRDriver.GetTipPositions.Options(
                TipSequence=self.PickupSequence,
                NumPositions=NumTips,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, FTRDriver.GetTipPositions.Response
        )

        return ResponseInstance.GetTipPositions()

    def _UpdateRemainingTips(self):
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

        self._RemainingTips = ResponseInstance.GetNumRemaining()
