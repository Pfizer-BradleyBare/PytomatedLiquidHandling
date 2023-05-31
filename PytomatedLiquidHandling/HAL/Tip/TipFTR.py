from ...Driver.Hamilton.Tip import FTR as FTRDriver
from .BaseTip import Tip
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class TipFTR(Tip):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        PickupSequence: str,
        MaxVolume: float,
    ):
        Tip.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            PickupSequence,
            MaxVolume,
        )

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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            self.GetBackend().GetResponse(CommandInstance, CommandInstance.Response)

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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.RemainingTips = ResponseInstance.GetNumRemaining()

        except:
            ...
