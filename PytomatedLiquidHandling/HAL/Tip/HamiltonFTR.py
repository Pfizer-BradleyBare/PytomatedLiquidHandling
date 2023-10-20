from typing import cast

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import HSLTipCountingLib
from .Base import TipABC


class HamiltonFTR(TipABC):
    def RemainingTipsInTier(self) -> int:
        return self.RemainingTips()

    def DiscardTierLayerToWaste(self):
        self.TipCounterEdit()

    def TipCounterEdit(self):
        ListedOptions = HSLTipCountingLib.Edit.ListedOptions(
            TipCounter="HamiltonTipFTR_" + str(self.MaxVolume) + "uL_TipCounter",
            DialogTitle="Please update the number of "
            + str(self.MaxVolume)
            + "uL tips currently loaded on the system",
        )
        for ID in self.RackLabwareIDs:
            ListedOptions.append(HSLTipCountingLib.Edit.Options(ID))

        CommandInstance = HSLTipCountingLib.Edit.Command(
            ListedOptions=ListedOptions,
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
