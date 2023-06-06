from math import ceil

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import PortraitCORE8Channel
from ..Pipette import TransferOptions
from .BasePipette import Pipette
from dataclasses import dataclass


@dataclass
class HamiltonPortraitCORE8Channel(Pipette):
    BackendInstance: HamiltonBackendABC
    ActiveChannels: list[int]

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def ConvertTransferVolumesToSupportedRange(
        self,
        OptionsTrackerInstance: TransferOptions.OptionsTracker,
    ) -> TransferOptions.OptionsTracker:
        MaxVolume = self.SupportedTipTrackerInstance.GetObjectsAsList()[
            -1
        ].TipInstance.MaxVolume

        UpdatedOptionsTrackerInstance = TransferOptions.OptionsTracker()
        for OptionsInstance in OptionsTrackerInstance.GetObjectsAsList():
            NumTransfers = ceil(OptionsInstance.TransferVolume / MaxVolume)
            OptionsInstance.TransferVolume /= NumTransfers

            for _ in range(0, NumTransfers):
                UpdatedOptionsTrackerInstance.LoadSingle(OptionsInstance)

        return UpdatedOptionsTrackerInstance

    def Transfer(
        self,
        OptionsTrackerInstance: TransferOptions.OptionsTracker,
    ):
        OptionsTrackerInstance = self.ConvertTransferVolumesToSupportedRange(
            OptionsTrackerInstance
        )

        OptionsListList: list[list[TransferOptions.Options]] = list()
        Counter = 0
        Options = OptionsTrackerInstance.GetObjectsAsList()
        NumOptions = len(Options)
        while Counter < NumOptions:
            OptionsListList.append(Options[Counter : Counter + 8])
            Counter += 8
        # Create a list of lists of options in packages of 8 because we can only transfer with 8 tips at a time

        for OptionsList in OptionsListList:
            RequiredTips: dict[str | int, int] = {
                Tip.TipInstance.UniqueIdentifier: 0
                for Tip in self.SupportedTipTrackerInstance.GetObjectsAsList()
            }
            for Options in OptionsList:
                RequiredTips[
                    self.GetTip(Options.TransferVolume).TipInstance.UniqueIdentifier
                ] += 1
            # How many tips of each volume do we need?

            TipPositions: dict[str | int, list[int]] = dict()
            for Tip, Count in RequiredTips.items():
                TipInstance = self.SupportedTipTrackerInstance.GetObjectByName(
                    Tip
                ).TipInstance
                TipInstance.UpdateTipPositions(Count)
                TipPositions[Tip] = TipInstance.TipPositions
            # Get our updated tip positions!

            PickupOptionsTracker = PortraitCORE8Channel.Pickup.OptionsTracker()
            AspirateOptionsTracker = PortraitCORE8Channel.Aspirate.OptionsTracker()
            DispenseOptionsTracker = PortraitCORE8Channel.Dispense.OptionsTracker()
            EjectOptionsTracker = PortraitCORE8Channel.Eject.OptionsTracker()
            for Count, Options in enumerate(OptionsList):
                PipetteTipInstance = self.GetTip(Options.TransferVolume)

                PickupOptionsTracker.LoadSingle(
                    PortraitCORE8Channel.Pickup.Options(
                        Sequence=PipetteTipInstance.TipInstance.PickupSequence,
                        ChannelNumber=Count,
                        SequencePosition=TipPositions[
                            PipetteTipInstance.UniqueIdentifier
                        ].pop(0),
                    )
                )

                AspirateOptionsTracker.LoadSingle(
                    PortraitCORE8Channel.Aspirate.Options(
                        ChannelNumber=Count,
                        Sequence=Options.SourceLayoutItemInstance.Sequence,
                        SequencePosition=Options.SourcePosition,
                        LiquidClass=str(
                            self.GetLiquidClass(
                                Options.SourceLiquidClassCategory,
                                Options.TransferVolume,
                            ).UniqueIdentifier
                        ),
                        Volume=Options.TransferVolume,
                    )
                )

                DispenseOptionsTracker.LoadSingle(
                    PortraitCORE8Channel.Dispense.Options(
                        ChannelNumber=Count,
                        Sequence=Options.DestinationLayoutItemInstance.Sequence,
                        SequencePosition=Options.DestinationPosition,
                        LiquidClass=str(
                            self.GetLiquidClass(
                                Options.DestinationLiquidClassCategory,
                                Options.TransferVolume,
                            ).UniqueIdentifier
                        ),
                        Volume=Options.TransferVolume,
                    )
                )

                EjectOptionsTracker.LoadSingle(
                    PortraitCORE8Channel.Eject.Options(
                        Sequence=PipetteTipInstance.WasteSequence,
                        ChannelNumber=Count,
                        SequencePosition=Count,
                    )
                )

            PortraitCORE8Channel.Pickup.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                OptionsTrackerInstance=PickupOptionsTracker,
            )
            PortraitCORE8Channel.Aspirate.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                OptionsTrackerInstance=AspirateOptionsTracker,
            )
            PortraitCORE8Channel.Dispense.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                OptionsTrackerInstance=DispenseOptionsTracker,
            )
            PortraitCORE8Channel.Eject.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                OptionsTrackerInstance=EjectOptionsTracker,
            )
