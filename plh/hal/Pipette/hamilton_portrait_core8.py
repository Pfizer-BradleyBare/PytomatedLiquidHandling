import itertools
from typing import DefaultDict, Literal, cast

from pydantic import dataclasses

from plh.hal import Labware

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.ML_STAR import Channel1000uL
from .Base import PipetteBase, PipetteTip, TransferOptions


@dataclasses.dataclass(kw_only=True)
class HamiltonPortraitCORE8Channel(PipetteBase):
    Backend: HamiltonBackendABC
    ActiveChannels: list[
        Literal[1]
        | Literal[2]
        | Literal[3]
        | Literal[4]
        | Literal[5]
        | Literal[6]
        | Literal[7]
        | Literal[8]
    ]

    def _GroupOptions(
        self,
        Options: list[TransferOptions],
    ) -> DefaultDict[str, list[tuple[PipetteTip, TransferOptions]]]:
        LiquidClassMaxVolumes: dict[str, float] = {}
        for Opt in Options:
            CombinedName = (
                Opt.SourceLiquidClassCategory + ":" + Opt.DestinationLiquidClassCategory
            )

            if CombinedName not in LiquidClassMaxVolumes:
                LiquidClassMaxVolumes[CombinedName] = self._GetMaxTransferVolume(
                    Opt.SourceLiquidClassCategory,
                    Opt.DestinationLiquidClassCategory,
                )
        # Max volume for each liquid class pairing. Important

        FinalTransferOptions: list[TransferOptions] = []
        TruncatedFinalTransferOptions: list[list[TransferOptions]] = []

        for Opt in Options:
            CombinedName = (
                Opt.SourceLiquidClassCategory + ":" + Opt.DestinationLiquidClassCategory
            )

            TruncatedOptions = self._TruncateTransferVolume(
                Opt,
                LiquidClassMaxVolumes[CombinedName],
            )

            if len(TruncatedOptions) == 1:
                FinalTransferOptions += TruncatedOptions
                # If there is only 1 option then no truncation occured. We want to perform all non truncated transfers first.
            else:
                TruncatedFinalTransferOptions.append(TruncatedOptions)
                # If there is more than one we want to collect them so we can shuffle. This may increaes final pipetting speed.=
        # Truncate based on max volume

        FinalTransferOptions += [
            i
            for l in itertools.zip_longest(
                *TruncatedFinalTransferOptions,
                fillvalue=None,
            )
            for i in l
            if i is not None
        ]
        # Shuffle our truncated options then add to the end.

        TipGroupedOptions: DefaultDict[
            str,
            list[tuple[PipetteTip, TransferOptions]],
        ] = DefaultDict(list)
        for Opt in Options:
            Tip = self._GetTip(
                Opt.SourceLiquidClassCategory,
                Opt.DestinationLiquidClassCategory,
                Opt.TransferVolume,
            )

            TipGroupedOptions[Tip.Tip.Identifier].append((Tip, Opt))
        return TipGroupedOptions

    def Transfer(self, Options: list[TransferOptions]):
        NumActiveChannels = len(self.ActiveChannels)

        TipGroupedOptions = self._GroupOptions(Options)

        for TipOptGroup in TipGroupedOptions.values():
            Tip = TipOptGroup[0][0]

            PackagedOpts = [
                [TipOpt[1] for TipOpt in TipOptGroup][x : x + NumActiveChannels]
                for x in range(0, len(TipOptGroup), NumActiveChannels)
            ]
            # Packaging in sets of num channels

            if len(PackagedOpts) > Tip.Tip.RemainingTips():
                raise RuntimeError("Not enough tips left")
            # are there at minimum enough tips left?

            for Opts in PackagedOpts:
                if Tip.Tip.RemainingTipsInTier() < len(Opts):
                    Tip.Tip.DiscardLayerToWaste()
                # If not enough tips then get user to help

                TipPositions = Tip.Tip._AvailablePositions[: len(Opts)]

                PickupOptions: list[Channel1000uL.Pickup.Options] = []
                for Index, (Opt, ChannelNumber) in enumerate(
                    zip(Opts, self.ActiveChannels),
                ):
                    PickupOptions.append(
                        Channel1000uL.Pickup.Options(
                            ChannelNumber=ChannelNumber,
                            LabwareID=TipPositions[Index].LabwareID,
                            PositionID=TipPositions[Index].PositionID,
                        ),
                    )
                Command = Channel1000uL.Pickup.Command(
                    BackendErrorHandling=self.BackendErrorHandling,
                    Options=PickupOptions,
                )
                self.Backend.ExecuteCommand(Command)
                self.Backend.GetResponse(Command, Channel1000uL.Pickup.Response)
                # Pickup the tips

                AspirateOptions: list[Channel1000uL.Aspirate.Options] = []
                for Index, (Opt, ChannelNumber) in enumerate(
                    zip(Opts, self.ActiveChannels),
                ):
                    AspirateLabware = cast(
                        Labware.PipettableLabware,
                        Opt.SourceLayoutItemInstance.Labware,
                    )

                    NumericAddressing = Labware.Base.Layout.Numeric(
                        Rows=Opt.SourceLayoutItemInstance.Labware.Wells.Layout.Rows,
                        Columns=Opt.SourceLayoutItemInstance.Labware.Wells.Layout.Columns,
                        Direction=Opt.SourceLayoutItemInstance.Labware.Wells.Layout.Direction,
                    )
                    # we need to do some numeric offsets to the position so convert it to a number first if it is not one.

                    AspiratePosition = (
                        (int(NumericAddressing.GetPositionID(Opt.SourcePosition)) - 1)
                        * AspirateLabware.Wells.PositionsPerWell
                        + Index
                        + 1
                    )
                    # The position MUST take into account the number of sequences per well.
                    # This calculates the proper position in the well for each channel if the container has multiple position positions.

                    AspirateOptions.append(
                        Channel1000uL.Aspirate.Options(
                            ChannelNumber=ChannelNumber,
                            LabwareID=Opt.SourceLayoutItemInstance.LabwareID,
                            PositionID=Opt.SourceLayoutItemInstance.Labware.Wells.Layout.GetPositionID(
                                AspiratePosition,
                            ),
                            LiquidClass=str(
                                self._GetLiquidClass(
                                    Opt.SourceLiquidClassCategory,
                                    Opt.TransferVolume,
                                ),
                            ),
                            Volume=Opt.TransferVolume,
                        ),
                    )

                Command = Channel1000uL.Aspirate.Command(
                    BackendErrorHandling=self.BackendErrorHandling,
                    Options=AspirateOptions,
                )
                self.Backend.ExecuteCommand(Command)
                self.Backend.GetResponse(Command, Channel1000uL.Aspirate.Response)

                DispenseOptions: list[Channel1000uL.Dispense.Options] = []
                for Index, (Opt, ChannelNumber) in enumerate(
                    zip(Opts, self.ActiveChannels),
                ):
                    DispenseLabware = cast(
                        Labware.PipettableLabware,
                        Opt.DestinationLayoutItemInstance.Labware,
                    )

                    NumericAddressing = Labware.Base.Layout.Numeric(
                        Rows=Opt.DestinationLayoutItemInstance.Labware.Wells.Layout.Rows,
                        Columns=Opt.DestinationLayoutItemInstance.Labware.Wells.Layout.Columns,
                        Direction=Opt.DestinationLayoutItemInstance.Labware.Wells.Layout.Direction,
                    )
                    # we need to do some numeric offsets to the position so convert it to a number first if it is not one.

                    DispensePosition = (
                        (
                            int(
                                NumericAddressing.GetPositionID(
                                    Opt.DestinationPosition,
                                ),
                            )
                            - 1
                        )
                        * DispenseLabware.Wells.PositionsPerWell
                        + Index
                        + 1
                    )
                    # The position MUST take into account the number of sequences per well.
                    # This calculates the proper position in the well for each channel if the container has multiple position positions.

                    DispenseOptions.append(
                        Channel1000uL.Dispense.Options(
                            ChannelNumber=ChannelNumber,
                            LabwareID=Opt.DestinationLayoutItemInstance.LabwareID,
                            PositionID=Opt.DestinationLayoutItemInstance.Labware.Wells.Layout.GetPositionID(
                                DispensePosition,
                            ),
                            LiquidClass=str(
                                self._GetLiquidClass(
                                    Opt.DestinationLiquidClassCategory,
                                    Opt.TransferVolume,
                                ),
                            ),
                            Volume=Opt.TransferVolume,
                        ),
                    )

                Command = Channel1000uL.Dispense.Command(
                    BackendErrorHandling=self.BackendErrorHandling,
                    Options=DispenseOptions,
                )
                self.Backend.ExecuteCommand(Command)
                self.Backend.GetResponse(Command, Channel1000uL.Dispense.Response)

                EjectPositions = ["1", "2", "3", "4", "13", "14", "15", "16"]
                # Hamilton waste always has 16 positions. Do be compatible with liquid waste we want to use the outer positions
                EjectOptions: list[Channel1000uL.Eject.Options] = []
                for Index, (Opt, ChannelNumber) in enumerate(
                    zip(Opts, self.ActiveChannels),
                ):
                    EjectOptions.append(
                        Channel1000uL.Eject.Options(
                            LabwareID=Tip.TipWasteLabwareID,
                            ChannelNumber=ChannelNumber,
                            PositionID=EjectPositions[Index],
                        ),
                    )

                Command = Channel1000uL.Eject.Command(
                    BackendErrorHandling=self.BackendErrorHandling,
                    Options=EjectOptions,
                )
                self.Backend.ExecuteCommand(Command)
                self.Backend.GetResponse(Command, Channel1000uL.Eject.Response)

    def TimeToTransfer(self, OptionsListInstance: list[TransferOptions]) -> float:
        return 0
