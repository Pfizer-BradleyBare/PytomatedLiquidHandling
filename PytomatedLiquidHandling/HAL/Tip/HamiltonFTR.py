from typing import cast

from ...Driver.Hamilton import HSLTipCountingLib
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .Base import TipABC


class HamiltonFTR(TipABC):
    def RemainingTipsInTier(self) -> int:
        return self.RemainingTips()

    def DiscardTierLayerToWaste(self):
        raise RuntimeError("FTR tips cannot waste tiers. Reload tips.")

    def TipCounterEdit(self):
        ListedOptions = HSLTipCountingLib.Edit.ListedOptions(
            TipCounter="HamiltonTipFTR_" + str(self.Volume) + "uL_TipCounter",
            DialogTitle="Please update the number of "
            + str(self.Volume)
            + "uL tips currently loaded on the system",
        )
        for TipRack in self.TipRacks:
            ListedOptions.append(HSLTipCountingLib.Edit.Options(TipRack.LabwareID))

        CommandInstance = HSLTipCountingLib.Edit.Command(
            Options=ListedOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self._ParseAvailablePositions(
            cast(
                list[dict[str, str]],
                self.Backend.GetResponse(
                    CommandInstance, HSLTipCountingLib.Edit.Response
                ).GetAvailablePositions(),
            )
        )
