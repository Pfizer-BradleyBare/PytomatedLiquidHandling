from dataclasses import dataclass
from math import ceil

from PytomatedLiquidHandling.HAL import Labware

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import PortraitCORE8Channel
from .Base import PipetteABC


@dataclass
class HamiltonPortraitCORE8Channel(PipetteABC):
    BackendInstance: HamiltonBackendABC
    ActiveChannels: list[int]

    def ConvertTransferVolumesToSupportedRange(
        self,
        ListedOptionsInstance: list[PipetteABC.TransferInterfaceCommand.Options],
    ) -> list[PipetteABC.TransferInterfaceCommand.Options]:
        MaxVolume = self.SupportedPipetteTips[-1].TipInstance.MaxVolume

        UpdatedListedOptionsInstance: list[
            PipetteABC.TransferInterfaceCommand.Options
        ] = list()
        for OptionsInstance in ListedOptionsInstance:
            NumTransfers = ceil(OptionsInstance.TransferVolume / MaxVolume)
            OptionsInstance.TransferVolume /= NumTransfers

            for _ in range(0, NumTransfers):
                UpdatedListedOptionsInstance.append(OptionsInstance)

        return UpdatedListedOptionsInstance

    def _Transfer(
        self,
        ListedOptionsInstance: list[PipetteABC.TransferInterfaceCommand.Options],
    ):
        ListedOptionsInstance = self.ConvertTransferVolumesToSupportedRange(
            ListedOptionsInstance
        )

        OptionsListList: list[
            list[PipetteABC.TransferInterfaceCommand.Options]
        ] = list()
        Counter = 0
        Options = ListedOptionsInstance
        NumOptions = len(Options)
        while Counter < NumOptions:
            OptionsListList.append(Options[Counter : Counter + 8])
            Counter += 8
        # Create a list of lists of options in packages of 8 because we can only transfer with 8 tips at a time

        for OptionsList in OptionsListList:
            RequiredTips: dict[str, int] = {
                Tip.TipInstance.Identifier: 0 for Tip in self.SupportedPipetteTips
            }
            # Package our tips for easy access

            for Options in OptionsList:
                RequiredTips[
                    self.GetTip(Options.TransferVolume).TipInstance.Identifier
                ] += 1
            # How many tips of each volume do we need?

            TipPositions: dict[str, list[int]] = dict()
            for Tip, Count in RequiredTips.items():
                TipInstance = None
                for PipetteTipInstance in self.SupportedPipetteTips:
                    if Tip == PipetteTipInstance.TipInstance.Identifier:
                        TipInstance = PipetteTipInstance.TipInstance
                        break

                if TipInstance is None:
                    raise Exception("")

                TipPositions[Tip] = TipInstance.GetTipPositions.Execute(
                    TipInstance.GetTipPositions.Options(NumTips=Count)
                )
            # Get our updated tip positions!

            ListedPickupOptions: list[PortraitCORE8Channel.Pickup.Options] = list()
            ListedAspirateOptions: list[PortraitCORE8Channel.Aspirate.Options] = list()
            ListedDispenseOptions: list[PortraitCORE8Channel.Dispense.Options] = list()
            ListedEjectOptions: list[PortraitCORE8Channel.Eject.Options] = list()
            for Count, Options in enumerate(OptionsList):
                PipetteTipInstance = self.GetTip(Options.TransferVolume)

                ListedPickupOptions.append(
                    PortraitCORE8Channel.Pickup.Options(
                        Sequence=PipetteTipInstance.TipInstance.PickupSequence,
                        ChannelNumber=Count + 1,
                        SequencePosition=TipPositions[
                            PipetteTipInstance.TipInstance.Identifier
                        ].pop(0),
                    )
                )

                AspirateLabware = Options.SourceLayoutItemInstance.LabwareInstance
                if not isinstance(AspirateLabware, Labware.PipettableLabware):
                    raise Exception("This should never happen")

                AspiratePosition = (
                    Options.SourcePosition
                    * AspirateLabware.LabwareWells.SequencesPerWell
                    + Count
                    + 1
                )

                ListedAspirateOptions.append(
                    PortraitCORE8Channel.Aspirate.Options(
                        ChannelNumber=Count + 1,
                        Sequence=Options.SourceLayoutItemInstance.Sequence,
                        SequencePosition=AspiratePosition,
                        LiquidClass=str(
                            self.GetLiquidClass(
                                Options.SourceLiquidClassCategory,
                                Options.TransferVolume,
                            ).Name
                        ),
                        Volume=Options.TransferVolume,
                    )
                )

                DispenseLabware = Options.SourceLayoutItemInstance.LabwareInstance
                if not isinstance(DispenseLabware, Labware.PipettableLabware):
                    raise Exception("This should never happen")

                DispensePosition = (
                    Options.SourcePosition
                    * DispenseLabware.LabwareWells.SequencesPerWell
                    + Count
                    + 1
                )

                ListedDispenseOptions.append(
                    PortraitCORE8Channel.Dispense.Options(
                        ChannelNumber=Count + 1,
                        Sequence=Options.DestinationLayoutItemInstance.Sequence,
                        SequencePosition=DispensePosition,
                        LiquidClass=str(
                            self.GetLiquidClass(
                                Options.DestinationLiquidClassCategory,
                                Options.TransferVolume,
                            ).Name
                        ),
                        Volume=Options.TransferVolume,
                    )
                )

                ListedEjectOptions.append(
                    PortraitCORE8Channel.Eject.Options(
                        Sequence=PipetteTipInstance.WasteSequence,
                        ChannelNumber=Count + 1,
                        SequencePosition=Count + 1,
                    )
                )

            print(
                PortraitCORE8Channel.Pickup.Command(
                    CustomErrorHandling=self.CustomErrorHandling,
                    ListedOptions=ListedPickupOptions,
                )
            )
            print(
                PortraitCORE8Channel.Aspirate.Command(
                    CustomErrorHandling=self.CustomErrorHandling,
                    ListedOptions=ListedAspirateOptions,
                )
            )
            print(
                PortraitCORE8Channel.Dispense.Command(
                    CustomErrorHandling=self.CustomErrorHandling,
                    ListedOptions=ListedDispenseOptions,
                )
            )
            print(
                PortraitCORE8Channel.Eject.Command(
                    CustomErrorHandling=self.CustomErrorHandling,
                    ListedOptions=ListedEjectOptions,
                )
            )

    def _TransferTime(
        self, ListedOptionsInstance: list[PipetteABC.TransferInterfaceCommand.Options]
    ) -> float:
        return 0
