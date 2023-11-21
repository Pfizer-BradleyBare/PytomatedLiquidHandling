from math import ceil
from typing import cast

from pydantic import field_validator

from PytomatedLiquidHandling.HAL import Labware

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.ML_STAR import Channel1000uL, CORE96Head
from . import HamiltonPortraitCORE8Channel
from .Base import PipetteABC, TransferOptions


class HamiltonCORE96Head(PipetteABC):
    Backend: HamiltonBackendABC
    HamiltonPortraitCORE8Channel: HamiltonPortraitCORE8Channel

    @field_validator("HamiltonPortraitCORE8Channel", mode="before")
    def __HamiltonPortraitCORE8ChannelValidate(cls, v):
        from . import Devices

        # Import here otherwise we get circular import error... Nature of the beast

        Objects = Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier + " is not found in " + PipetteABC.__name__ + " objects."
            )

        return Objects[Identifier]

    def Transfer(self, Options: list[TransferOptions]):
        Opt = Options[0]
        # All the options should be the same. So we can just take the first one for the majority

        MaxVolume = self._GetMaxTransferVolume(
            Opt.SourceLiquidClassCategory, Opt.DestinationLiquidClassCategory
        )

        NumRepeats = ceil(Opt.TransferVolume / MaxVolume)
        TransferVolume = Opt.TransferVolume / NumRepeats
        # Find out how many transfers we need to do

        Tip = self._GetTip(
            Opt.SourceLiquidClassCategory,
            Opt.DestinationLiquidClassCategory,
            TransferVolume,
        )

        NumActiveChannels = len(self.HamiltonPortraitCORE8Channel.ActiveChannels)

        PackagedOpts = [
            Options[x : x + NumActiveChannels]
            for x in range(0, len(Options), NumActiveChannels)
        ]

        for Opts in PackagedOpts:
            if Tip.Tip.RemainingTipsInTier() < len(Opts):
                Tip.Tip.DiscardTierLayerToWaste()
            # If not enough tips then get user to help

            TipPositions = Tip.Tip._AvailablePositions[: len(Opts)]

            SupportPickupOptions: list[Channel1000uL.Pickup.Options] = list()
            for Index, (Opt, ChannelNumber) in enumerate(
                zip(Opts, self.HamiltonPortraitCORE8Channel.ActiveChannels)
            ):
                SupportPickupOptions.append(
                    Channel1000uL.Pickup.Options(
                        ChannelNumber=ChannelNumber,
                        LabwareID=TipPositions[Index].LabwareID,
                        PositionID=TipPositions[Index].PositionID,
                    )
                )
            Command = Channel1000uL.Pickup.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=SupportPickupOptions,
            )
            self.Backend.ExecuteCommand(Command)
            self.Backend.GetResponse(Command, Channel1000uL.Pickup.Response)
            # Pickup the tips

            NumericAddressing = Labware.Base.Layout.Numeric()
            # Hamilton tip positions are always numeric and are always sorted columwise.
            # So we are going to convert the desired pipetting positions to the correct numeric position

            SupportEjectOptions: list[Channel1000uL.Eject.Options] = list()
            for Index, (Opt, ChannelNumber) in enumerate(
                zip(Opts, self.HamiltonPortraitCORE8Channel.ActiveChannels)
            ):
                SupportEjectOptions.append(
                    Channel1000uL.Eject.Options(
                        LabwareID=Tip.TipSupportDropoffLabwareID,
                        ChannelNumber=ChannelNumber,
                        PositionID=NumericAddressing.GetPositionID(
                            Opt.SourcePosition  # Source and destination are the same
                        ),
                    )
                )

            Command = Channel1000uL.Eject.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=SupportEjectOptions,
            )
            self.Backend.ExecuteCommand(Command)
            self.Backend.GetResponse(Command, Channel1000uL.Eject.Response)
            # Eject into the tip support at the correct position
        # This picks up tips with the 1mL channels and ejects them in the tip support rack. The 96 head will now pick them up.

        PickupOptions = CORE96Head.Pickup.Options(
            LabwareID=Tip.TipSupportPickupLabwareID
        )
        Command = CORE96Head.Pickup.Command(
            CustomErrorHandling=self.CustomErrorHandling,
            Options=PickupOptions,
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.GetResponse(Command, CORE96Head.Pickup.Response)

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

        for _ in range(0, NumRepeats):
            Command = CORE96Head.Aspirate.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=AspirateOptions,
            )
            self.Backend.ExecuteCommand(Command)
            self.Backend.GetResponse(Command, CORE96Head.Aspirate.Response)

            Command = CORE96Head.Dispense.Command(
                CustomErrorHandling=self.CustomErrorHandling,
                Options=DispenseOptions,
            )
            self.Backend.ExecuteCommand(Command)
            self.Backend.GetResponse(Command, CORE96Head.Dispense.Response)

        EjectOptions = CORE96Head.Eject.Options(LabwareID=Tip.TipWasteLabwareID)
        Command = CORE96Head.Eject.Command(
            CustomErrorHandling=self.CustomErrorHandling,
            Options=EjectOptions,
        )
        self.Backend.ExecuteCommand(Command)
        self.Backend.GetResponse(Command, CORE96Head.Eject.Response)

    def TimeToTransfer(self, Options: list[TransferOptions]) -> float:
        return 0
