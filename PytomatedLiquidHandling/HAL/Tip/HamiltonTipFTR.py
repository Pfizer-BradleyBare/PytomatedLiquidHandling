from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .BaseTip import Tip
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from dataclasses import dataclass


@dataclass
class HamiltonTipFTR(Tip):
    BackendInstance: HamiltonBackendABC

    def Initialize(self):
        self.Reload()

    def Deinitialize(self):
        ...

    def Reload(self):
        try:
            CommandInstance = FTRDriver.LoadTips.Command(
                OptionsInstance=FTRDriver.LoadTips.Options(
                    TipSequence=self.PickupSequence
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            self.BackendInstance.GetResponse(CommandInstance, CommandInstance.Response)

        except:
            ...

        # We also need to show a deck loading dialog, move the autoload, etc.

    def UpdateTipPositions(self, *, NumTips: int):
        try:
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
                CommandInstance, CommandInstance.Response
            )

            self.TipPositions = ResponseInstance.GetTipPositions()

        except:
            ...

    def UpdateRemainingTips(self):
        try:
            CommandInstance = FTRDriver.GetNumTips.Command(
                OptionsInstance=FTRDriver.GetNumTips.Options(
                    TipSequence=self.PickupSequence,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.RemainingTips = ResponseInstance.GetNumRemaining()

        except:
            ...
