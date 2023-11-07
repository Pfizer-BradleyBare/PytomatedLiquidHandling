from math import ceil

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import CORE96Head
from .Base import ListedTransferOptions, PipetteABC, TransferOptions


class HamiltonCORE96Head(PipetteABC):
    Backend: HamiltonBackendABC

    def Transfer(
        self,
        Options: ListedTransferOptions | list[ListedTransferOptions],
    ):
        Opt = Options[0]
        # All the options should be the same. So we can just take the first one for the majority

        MaxVolume = self.SupportedTips[-1].Tip.Volume
        NumTransfers = ceil(Opt.TransferVolume / MaxVolume)
        TransferVolume = Opt.TransferVolume / NumTransfers
        # Find out how many transfers we need to do

        PipetteTipInstance = self.GetTip(TransferVolume)

        PickupOptions = CORE96Head.Pickup.Options(
            Sequence=PipetteTipInstance.Tip.PickupSequence
        )

        AspirateOptions = CORE96Head.Aspirate.Options(
            Sequence=Options.SourceLayoutItemInstance.Sequence,
            LiquidClass=str(
                self.GetLiquidClass(
                    Options.SourceLiquidClassCategory, TransferVolume
                ).Name
            ),
            Volume=TransferVolume,
        )

        DispenseOptions = CORE96Head.Dispense.Options(
            Sequence=Options.SourceLayoutItemInstance.Sequence,
            LiquidClass=str(
                self.GetLiquidClass(
                    Options.SourceLiquidClassCategory, TransferVolume
                ).Name
            ),
            Volume=TransferVolume,
        )

        EjectOptions = CORE96Head.Eject.Options(
            Sequence=PipetteTipInstance.WasteSequence
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

    def TimeToTransfer(
        self, OptionsTracker: ListedTransferOptions | list[ListedTransferOptions]
    ) -> float:
        return 0
