from math import ceil
from typing import cast

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import CORE96Head
from .Base import PipetteABC, TransferOptions


class HamiltonCORE96Head(PipetteABC):
    Backend: HamiltonBackendABC

    def Transfer(
        self,
        Options: list[TransferOptions] | list[list[TransferOptions]],
    ):
        if len(Options) == 0:
            raise ValueError("No items in Options list")

        if all(isinstance(Opts, TransferOptions) for Opts in Options):
            Options = [cast(list[TransferOptions], Options)]
        Options = cast(list[list[TransferOptions]], Options)
        # We will always assume it is a list of pipetting steps in the following code.

        for ListedOptions in Options:
            Opt = ListedOptions[0]
            # All the options should be the same. So we can just take the first one for the majority

            MaxVolume = self.SupportedTips[-1].Tip.Volume
            NumTransfers = ceil(Opt.TransferVolume / MaxVolume)
            TransferVolume = Opt.TransferVolume / NumTransfers
            # Find out how many transfers we need to do

            PipetteTipInstance = self._GetTip(
                Opt.SourceLiquidClassCategory,
                Opt.DestinationLiquidClassCategory,
                TransferVolume,
            )

            PickupOptions = CORE96Head.Pickup.Options(
                LabwareID=PipetteTipInstance.Tip.PickupSequence
            )

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
