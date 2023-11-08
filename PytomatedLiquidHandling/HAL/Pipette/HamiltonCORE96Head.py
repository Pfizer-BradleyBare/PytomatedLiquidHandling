from math import ceil
from typing import cast

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import CORE96Head
from .Base import PipetteABC, TransferOptions


class HamiltonCORE96Head(PipetteABC):
    Backend: HamiltonBackendABC

    def Transfer(self, Options: list[TransferOptions]):
        Opt = Options[0]
        # All the options should be the same. So we can just take the first one for the majority

        MaxVolume = self._GetMaxTransferVolume(
            Opt.SourceLiquidClassCategory, Opt.DestinationLiquidClassCategory
        )

        NumTransfers = ceil(Opt.TransferVolume / MaxVolume)
        TransferVolume = Opt.TransferVolume / NumTransfers
        # Find out how many transfers we need to do

        PipetteTipInstance = self._GetTip(
            Opt.SourceLiquidClassCategory,
            Opt.DestinationLiquidClassCategory,
            TransferVolume,
        )

        PickupOptions = CORE96Head.Pickup.Options(
            LabwareID=PipetteTipInstance.Tip.RackLabwareIDs[0]
        )
        # TODO. Need to use 1mL channels to move the tips to the support rack

        AspirateOptions = CORE96Head.Aspirate.Options(
            LabwareID=Opt.SourceLayoutItemInstance.LabwareID,
            LiquidClass=str(
                self._GetLiquidClass(
                    Opt.SourceLiquidClassCategory,
                    TransferVolume,
                )
            ),
            Volume=TransferVolume,
        )

        DispenseOptions = CORE96Head.Dispense.Options(
            LabwareID=Opt.SourceLayoutItemInstance.LabwareID,
            LiquidClass=str(
                self._GetLiquidClass(Opt.SourceLiquidClassCategory, TransferVolume)
            ),
            Volume=TransferVolume,
        )

        EjectOptions = CORE96Head.Eject.Options(
            LabwareID=PipetteTipInstance.TipWasteLabwareID
        )

        for _ in range(0, NumTransfers):
            CORE96Head.Pickup.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=PickupOptions,
            )

            CORE96Head.Aspirate.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=AspirateOptions,
            )

            CORE96Head.Dispense.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=DispenseOptions,
            )

            CORE96Head.Eject.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=EjectOptions,
            )

    def TimeToTransfer(self, Options: list[TransferOptions]) -> float:
        return 0
