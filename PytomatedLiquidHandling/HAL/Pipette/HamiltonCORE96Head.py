from dataclasses import dataclass
from math import ceil

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import CORE96Head
from .BasePipette import Pipette


@dataclass
class HamiltonCORE96Head(Pipette):
    BackendInstance: HamiltonBackendABC

    def OptionsSupported(
        self, ListedOptionsInstance: list[Pipette.TransferInterfaceCommand.Options]
    ) -> bool:
        if (
            len(
                set(
                    [
                        Options.SourceLayoutItemInstance
                        for Options in ListedOptionsInstance
                    ]
                )
            )
            > 1
        ):
            return False
        if (
            len(
                set(
                    [
                        Options.DestinationLayoutItemInstance
                        for Options in ListedOptionsInstance
                    ]
                )
            )
            > 1
        ):
            return False
        # Should be a single sequence location

        if len(set([Options.TransferVolume for Options in ListedOptionsInstance])) > 1:
            return False
        # Transfer volume should be same for all wells

        if len(
            set([Options.SourcePosition for Options in ListedOptionsInstance])
        ) != len([Options.SourcePosition for Options in ListedOptionsInstance]):
            return False
        if len(
            set([Options.DestinationPosition for Options in ListedOptionsInstance])
        ) != len([Options.DestinationPosition for Options in ListedOptionsInstance]):
            return False
        # Well positions should not repeat

        SourcePositionHolder = 0
        DestinationPositionHolder = 0
        for Options in ListedOptionsInstance:
            if not Options.DestinationPosition == Options.SourcePosition:
                return False
            # Source and destination positions MUST be the same

            if not Options.SourcePosition > SourcePositionHolder:
                return False
            SourcePositionHolder = Options.SourcePosition
            if not Options.DestinationPosition > DestinationPositionHolder:
                return False
            DestinationPositionHolder = Options.DestinationPosition
            # Positions should go in increasing order

        if len(ListedOptionsInstance) > 96:
            return False
        # Only 96 channels are supported.

        return Pipette.OptionsSupported(self, ListedOptionsInstance)
        # Check all other requirements

    def _Transfer(
        self,
        ListedOptionsInstance: list[Pipette.TransferInterfaceCommand.Options],
    ):
        Options = ListedOptionsInstance[0]
        # All the options should be the same. So we can just take the first one for the majority

        MaxVolume = self.SupportedPipetteTips[-1].TipInstance.MaxVolume
        NumTransfers = ceil(Options.TransferVolume / MaxVolume)
        TransferVolume = Options.TransferVolume / NumTransfers
        # Find out how many transfers we need to do

        PipetteTipInstance = self.GetTip(TransferVolume)

        PickupOptions = CORE96Head.Pickup.Options(
            Sequence=PipetteTipInstance.TipInstance.PickupSequence
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

    def _TransferTime(
        self, OptionsTrackerInstance: list[Pipette.TransferInterfaceCommand.Options]
    ) -> float:
        return 0
