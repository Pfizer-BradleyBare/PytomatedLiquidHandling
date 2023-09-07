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

    def _TipCounterEdit(self):
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

    def _TipCounterEditTime(self) -> float:
        return 0

    def _GetTipPositions(
        self, Options: TipABC.GetTipPositionsInterfaceCommand.Options
    ) -> list[int]:
        CommandInstance = NTRDriver.GetTipPositions.Command(
            Options=NTRDriver.GetTipPositions.Options(
                TipSequence=self.PickupSequence,
                GeneratedRackWasteSequence=self.GeneratedWasteSequence,
                GripperSequence=self.GripperSequence,
                NumPositions=Options.NumTips,
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
        self, Options: TipABC.GetTipPositionsInterfaceCommand.Options
    ) -> float:
        return 0

    def _GetRemainingTips(self) -> int:
        CommandInstance = NTRDriver.GetNumTips.Command(
            Options=NTRDriver.GetNumTips.Options(
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
