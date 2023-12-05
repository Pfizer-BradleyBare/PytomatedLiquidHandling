from typing import Literal, cast
from pydantic import BaseModel
from PytomatedLiquidHandling.Driver.Hamilton import Backend, HSLTipCountingLib
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import TipABC


class HamiltonEETR(TipABC):
    class TipStack(BaseModel):
        TipRack: LayoutItem.TipRack
        ModuleNumber: int
        StackNumber: int

    Backend: Backend.HamiltonBackendABC
    CustomErrorHandling: Literal["N/A"] = "N/A"

    TipStacks: list[TipStack]
    TipRackWasteLabwareID: str

    def RemainingTips(self) -> int:
        ...

    def RemainingTipsInTier(self) -> int:
        return TipABC.RemainingTips(self)

    def DiscardTierLayerToWaste(self):
        ...
        # TODO

    def TipCounterEdit(self):
        CommandInstance = HSLTipCountingLib.Edit.Command(
            Options=HSLTipCountingLib.Edit.ListedOptions(
                TipCounter="HamiltonTipFTR_" + str(self.Volume) + "uL_TipCounter",
                DialogTitle="Please update the number of "
                + str(self.Volume)
                + "uL tips currently loaded on the system",
            )
        )
        for TipRack in self.TipRacks:
            CommandInstance.Options.append(
                HSLTipCountingLib.Edit.Options(LabwareID=TipRack.LabwareID)
            )

        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self._ParseAvailablePositions(
            cast(
                list[dict[str, str]],
                self.Backend.GetResponse(
                    CommandInstance, HSLTipCountingLib.Edit.Response
                ).AvailablePositions,
            )
        )
