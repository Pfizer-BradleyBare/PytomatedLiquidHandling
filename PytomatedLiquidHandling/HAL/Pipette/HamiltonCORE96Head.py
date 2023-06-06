from math import ceil
from PytomatedLiquidHandling.HAL.Pipette.BasePipette.Interface import TransferOptions
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ..DeckLocation import DeckLocationTracker
from ..Labware import LabwareTracker
from ..Pipette import TransferOptions
from .BasePipette import LiquidClassCategoryTracker, Pipette, PipetteTipTracker
from ...Driver.Hamilton.Pipette import CORE96Head, PortraitCORE8Channel


class HamiltonCORE96Head(Pipette):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        SupportedTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
        SupportedDeckLocationTrackerInstance: DeckLocationTracker,
        SupportedLiquidClassCategoryTrackerInstance: LiquidClassCategoryTracker,
    ):
        Pipette.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            SupportedTipTrackerInstance,
            SupportedLabwareTrackerInstance,
            SupportedDeckLocationTrackerInstance,
            SupportedLiquidClassCategoryTrackerInstance,
        )

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def OptionsSupported(
        self, OptionsTrackerInstance: TransferOptions.OptionsTracker
    ) -> bool:
        if (
            len(
                set(
                    [
                        Options.SourceLayoutItemInstance
                        for Options in OptionsTrackerInstance.GetObjectsAsList()
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
                        for Options in OptionsTrackerInstance.GetObjectsAsList()
                    ]
                )
            )
            > 1
        ):
            return False
        # Should be a single sequence location

        if (
            len(
                set(
                    [
                        Options.TransferVolume
                        for Options in OptionsTrackerInstance.GetObjectsAsList()
                    ]
                )
            )
            > 1
        ):
            return False
        # Transfer volume should be same for all wells

        if len(
            set(
                [
                    Options.SourcePosition
                    for Options in OptionsTrackerInstance.GetObjectsAsList()
                ]
            )
        ) != len(
            [
                Options.SourcePosition
                for Options in OptionsTrackerInstance.GetObjectsAsList()
            ]
        ):
            return False
        if len(
            set(
                [
                    Options.DestinationPosition
                    for Options in OptionsTrackerInstance.GetObjectsAsList()
                ]
            )
        ) != len(
            [
                Options.DestinationPosition
                for Options in OptionsTrackerInstance.GetObjectsAsList()
            ]
        ):
            return False
        # Well positions should not repeat

        SourcePositionHolder = 0
        DestinationPositionHolder = 0
        for Options in OptionsTrackerInstance.GetObjectsAsList():
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

        if len(OptionsTrackerInstance.GetObjectsAsList()) > 96:
            return False
        # Only 96 channels are supported.

        return Pipette.OptionsSupported(self, OptionsTrackerInstance)
        # Check all other requirements

    def Transfer(
        self,
        OptionsTrackerInstance: TransferOptions.OptionsTracker,
    ):
        Options = OptionsTrackerInstance.GetObjectsAsList()[0]
        # All the options should be the same. So we can just take the first one for the majority

        MaxVolume = self.SupportedTipTrackerInstance.GetObjectsAsList()[
            -1
        ].TipInstance.MaxVolume
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
                ).GetUniqueIdentifier()
            ),
            Volume=TransferVolume,
        )

        DispenseOptions = CORE96Head.Dispense.Options(
            Sequence=Options.SourceLayoutItemInstance.Sequence,
            LiquidClass=str(
                self.GetLiquidClass(
                    Options.SourceLiquidClassCategory, TransferVolume
                ).GetUniqueIdentifier()
            ),
            Volume=TransferVolume,
        )

        EjectOptions = CORE96Head.Eject.Options(
            Sequence=PipetteTipInstance.WasteSequence
        )

        for _ in range(0, NumTransfers):
            CORE96Head.Pickup.Command(
                CustomErrorHandling=self.GetErrorHandlingSetting(),
                OptionsInstance=PickupOptions,
            )

            CORE96Head.Aspirate.Command(
                CustomErrorHandling=self.GetErrorHandlingSetting(),
                OptionsInstance=AspirateOptions,
            )

            CORE96Head.Dispense.Command(
                CustomErrorHandling=self.GetErrorHandlingSetting(),
                OptionsInstance=DispenseOptions,
            )

            CORE96Head.Eject.Command(
                CustomErrorHandling=self.GetErrorHandlingSetting(),
                OptionsInstance=EjectOptions,
            )
