from math import ceil
from typing import Any

from PytomatedLiquidHandling.HAL import Labware

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Pipette import PortraitCORE8Channel
from .Base import PipetteABC, TransferOptions


class HamiltonPortraitCORE8Channel(PipetteABC):
    Backend: HamiltonBackendABC
    ActiveChannels: list[int]

    def _TruncateTransferVolume(
        self, TransferOptions: TransferOptions, Volume: float
    ) -> list[TransferOptions]:
        UpdatedListedOptions = list()

        NumTransfers = ceil(TransferOptions.TransferVolume / Volume)
        TransferOptions.TransferVolume /= NumTransfers

        for _ in range(0, NumTransfers):
            UpdatedListedOptions.append(TransferOptions)

        return UpdatedListedOptions

    def Transfer(
        self,
        ListedOptions: list[TransferOptions],
    ):
        ListedOptions = [
            NewOptions
            for Options in ListedOptions
            for NewOptions in self._TruncateTransferVolume(
                Options,
                self._GetTip(
                    Options.SourceLiquidClassCategory,
                    Options.DestinationLiquidClassCategory,
                    Options.TransferVolume,
                ).Tip.Volume,
            )
        ]
        # Use the appropriate tip to determine how many transfers will occur.

        OptionsListList: list[list[TransferOptions]] = list()
        Counter = 0
        NumOptions = len(ListedOptions)
        while Counter < NumOptions:
            OptionsListList.append(ListedOptions[Counter : Counter + 8])
            Counter += 8
        # Create a list of lists of options in packages of 8 because we can only transfer with 8 tips at a time

        for OptionsList in OptionsListList:
            RequiredTips: dict[str, int] = {
                Tip.Tip.Identifier: 0 for Tip in self.SupportedTips
            }
            # Package our tips for easy access

            for Options in OptionsList:
                RequiredTips[
                    self._GetTip(
                        Options.SourceLiquidClassCategory,
                        Options.DestinationLiquidClassCategory,
                        Options.TransferVolume,
                    ).Tip.Identifier
                ] += 1
            # How many tips of each volume do we need?

            TipPositions: dict[str, list[Any]] = dict()
            for Tip, Count in RequiredTips.items():
                TipInstance = None
                for PipetteTipInstance in self.SupportedTips:
                    if Tip == PipetteTipInstance.Tip.Identifier:
                        TipInstance = PipetteTipInstance.Tip
                        break

                if TipInstance is None:
                    raise Exception("")

                if TipInstance.RemainingTips() < Count:
                    TipInstance.DiscardTierLayerToWaste()
                # If we don't have enough tips then try to get a user to help out

                TipPositions[Tip] = TipInstance._AvailablePositions[:8]
                TipInstance._AvailablePositions = TipInstance._AvailablePositions[8:]
            # Get our updated tip positions!

            ListedPickupOptions: list[PortraitCORE8Channel.Pickup.Options] = list()
            ListedAspirateOptions: list[PortraitCORE8Channel.Aspirate.Options] = list()
            ListedDispenseOptions: list[PortraitCORE8Channel.Dispense.Options] = list()
            ListedEjectOptions: list[PortraitCORE8Channel.Eject.Options] = list()
            for Count, Options in enumerate(OptionsList):
                PipetteTipInstance = self._GetTip(
                    Options.SourceLiquidClassCategory,
                    Options.DestinationLiquidClassCategory,
                    Options.TransferVolume,
                )

                ListedPickupOptions.append(
                    PortraitCORE8Channel.Pickup.Options(
                        LabwareID=TipPositions[PipetteTipInstance.Tip.Identifier].pop(
                            0
                        )["LabwareID"],
                        PositionID=TipPositions[PipetteTipInstance.Tip.Identifier].pop(
                            0
                        )["PositionID"],
                        ChannelNumber=Count + 1,
                    )
                )

                AspirateLabware = Options.SourceLayoutItemInstance.Labware
                if not isinstance(AspirateLabware, Labware.PipettableLabware):
                    raise Exception("This should never happen")

                NumericAddressing = Labware.Base.Addressing.NumericAddressing(
                    Rows=Options.SourceLayoutItemInstance.Labware.Wells.Addressing.Rows,
                    Columns=Options.SourceLayoutItemInstance.Labware.Wells.Addressing.Columns,
                    Direction=Options.SourceLayoutItemInstance.Labware.Wells.Addressing.Direction,
                )

                AspiratePosition = (
                    int(NumericAddressing.GetPosition(Options.SourcePosition))
                    * AspirateLabware.Wells.SequencesPerWell
                    + Count
                    + 1
                )

                ListedAspirateOptions.append(
                    PortraitCORE8Channel.Aspirate.Options(
                        ChannelNumber=Count + 1,
                        LabwareID=Options.SourceLayoutItemInstance.LabwareID,
                        PositionID=Options.SourceLayoutItemInstance.Labware.Wells.Addressing.GetPosition(
                            Labware.Base.Addressing.NumericPosition(AspiratePosition)
                        ),
                        LiquidClass=str(
                            self._GetLiquidClass(
                                Options.SourceLiquidClassCategory,
                                Options.TransferVolume,
                            )
                        ),
                        Volume=Options.TransferVolume,
                    )
                )

                DispenseLabware = Options.SourceLayoutItemInstance.Labware
                if not isinstance(DispenseLabware, Labware.PipettableLabware):
                    raise Exception("This should never happen")

                NumericAddressing = Labware.Base.Addressing.NumericAddressing(
                    Rows=Options.DestinationLayoutItemInstance.Labware.Wells.Addressing.Rows,
                    Columns=Options.DestinationLayoutItemInstance.Labware.Wells.Addressing.Columns,
                    Direction=Options.DestinationLayoutItemInstance.Labware.Wells.Addressing.Direction,
                )

                DispensePosition = (
                    int(NumericAddressing.GetPosition(Options.DestinationPosition))
                    * DispenseLabware.Wells.SequencesPerWell
                    + Count
                    + 1
                )

                ListedDispenseOptions.append(
                    PortraitCORE8Channel.Dispense.Options(
                        ChannelNumber=Count + 1,
                        LabwareID=Options.DestinationLayoutItemInstance.LabwareID,
                        PositionID=Options.DestinationLayoutItemInstance.Labware.Wells.Addressing.GetPosition(
                            Labware.Base.Addressing.NumericPosition(DispensePosition)
                        ),
                        LiquidClass=str(
                            self._GetLiquidClass(
                                Options.DestinationLiquidClassCategory,
                                Options.TransferVolume,
                            )
                        ),
                        Volume=Options.TransferVolume,
                    )
                )

                ListedEjectOptions.append(
                    PortraitCORE8Channel.Eject.Options(
                        LabwareID=PipetteTipInstance.TipWasteLabwareID,
                        ChannelNumber=Count + 1,
                        PositionID=str(Count + 1),
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

    def TransferTime(self, ListedOptionsInstance: list[TransferOptions]) -> float:
        return 0
