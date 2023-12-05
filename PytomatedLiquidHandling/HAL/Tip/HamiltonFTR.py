from typing import Literal, cast

from PytomatedLiquidHandling.Driver.Hamilton import Backend, HSLTipCountingLib

from .Base import TipABC


class HamiltonFTR(TipABC):
    Backend: Backend.HamiltonBackendABC
    CustomErrorHandling: Literal["N/A"] = "N/A"

    def RemainingTipsInTier(self) -> int:
        return self.RemainingTips()

    def DiscardLayerToWaste(self):
        raise RuntimeError("FTR tips cannot waste tiers. Reload tips.")

    def UpdateAvailablePositions(self):
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
