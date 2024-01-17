from __future__ import annotations

from math import ceil

from pydantic import dataclasses, field_validator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uL, CORE96Head
from plh.hal import labware

from .hamilton_portrait_core8 import HamiltonPortraitCORE8
from .pipette_base import PipetteBase, TransferOptions


@dataclasses.dataclass(kw_only=True)
class HamiltonCORE96(PipetteBase):
    backend: HamiltonBackendBase
    hamilton_portrait_core_8: HamiltonPortraitCORE8

    @field_validator("hamilton_portrait_core_8", mode="before")
    @classmethod
    def __hamilton_portrait_core_8_validate(
        cls: type[HamiltonCORE96],
        v: str | PipetteBase,
    ) -> PipetteBase:
        if isinstance(v, PipetteBase):
            return v

        from . import devices

        # Import here otherwise we get circular import error... Nature of the beast

        objects = devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier + " is not found in " + PipetteBase.__name__ + " objects.",
            )

        return objects[identifier]

    def transfer(self: HamiltonCORE96, options: list[TransferOptions]) -> None:
        opt = options[0]
        # All the options should be the same. So we can just take the first one for the majority

        max_volume = self._get_max_transfer_volume(
            opt.SourceLiquidClassCategory,
            opt.DestinationLiquidClassCategory,
        )

        num_repeats = ceil(opt.TransferVolume / max_volume)
        transfer_volume = opt.TransferVolume / num_repeats
        # Find out how many transfers we need to do

        tip = self._get_tip(
            opt.SourceLiquidClassCategory,
            opt.DestinationLiquidClassCategory,
            transfer_volume,
        )

        num_active_channels = len(self.hamilton_portrait_core_8.active_channels)

        packaged_opts = [
            options[x : x + num_active_channels]
            for x in range(0, len(options), num_active_channels)
        ]

        for opts in packaged_opts:
            if tip.tip.remaining_tips_in_tier() < len(opts):
                tip.tip.discard_layer_to_waste()
            # If not enough tips then get user to help

            tip_positions = tip.tip.available_positions[: len(opts)]

            support_pickup_options: list[Channel1000uL.Pickup.Options] = []
            for index, (opt, channel_number) in enumerate(
                zip(opts, self.hamilton_portrait_core_8.active_channels),
            ):
                support_pickup_options.append(
                    Channel1000uL.Pickup.Options(
                        ChannelNumber=channel_number,
                        LabwareID=tip_positions[index].LabwareID,
                        PositionID=tip_positions[index].PositionID,
                    ),
                )
            command = Channel1000uL.Pickup.Command(
                backend_error_handling=self.backend_error_handling,
                options=support_pickup_options,
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(command, Channel1000uL.Pickup.Response)
            # Pickup the tips

            numeric_layout = labware.NumericLayout(
                rows=8,
                columns=12,
                direction=labware.LayoutSorting.Columnwise,
            )
            # Hamilton tip positions are always numeric and are always sorted columwise.
            # So we are going to convert the desired pipetting positions to the correct numeric position

            support_eject_options: list[Channel1000uL.Eject.Options] = []
            for index, (opt, channel_number) in enumerate(
                zip(opts, self.hamilton_portrait_core_8.active_channels),
            ):
                support_eject_options.append(
                    Channel1000uL.Eject.Options(
                        LabwareID=tip.tip_support_dropoff_labware_id,
                        ChannelNumber=channel_number,
                        PositionID=numeric_layout.get_position_id(
                            opt.SourcePosition,  # Source and destination are the same
                        ),
                    ),
                )

            command = Channel1000uL.Eject.Command(
                backend_error_handling=self.backend_error_handling,
                options=support_eject_options,
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(command, Channel1000uL.Eject.Response)
            # Eject into the tip support at the correct position
        # This picks up tips with the 1mL channels and ejects them in the tip support rack. The 96 head will now pick them up.

        pickup_options = CORE96Head.Pickup.Options(
            LabwareID=tip.tip_support_pickup_labware_id,
        )
        command = CORE96Head.Pickup.Command(
            backend_error_handling=self.backend_error_handling,
            options=pickup_options,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, CORE96Head.Pickup.Response)

        aspirate_options = CORE96Head.Aspirate.Options(
            LabwareID=opt.SourceLayoutItemInstance.labware_id,
            LiquidClass=str(
                self._get_liquid_class(
                    opt.SourceLiquidClassCategory,
                    transfer_volume,
                ),
            ),
            Volume=transfer_volume,
        )

        dispense_options = CORE96Head.Dispense.Options(
            LabwareID=opt.SourceLayoutItemInstance.labware_id,
            LiquidClass=str(
                self._get_liquid_class(opt.SourceLiquidClassCategory, transfer_volume),
            ),
            Volume=transfer_volume,
        )

        for _ in range(num_repeats):
            command = CORE96Head.Aspirate.Command(
                backend_error_handling=self.backend_error_handling,
                options=aspirate_options,
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(command, CORE96Head.Aspirate.Response)

            command = CORE96Head.Dispense.Command(
                backend_error_handling=self.backend_error_handling,
                options=dispense_options,
            )
            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(command, CORE96Head.Dispense.Response)

        eject_options = CORE96Head.Eject.Options(LabwareID=tip.tip_waste_labware_id)
        command = CORE96Head.Eject.Command(
            backend_error_handling=self.backend_error_handling,
            options=eject_options,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, CORE96Head.Eject.Response)

    def time_to_transfer(self: HamiltonCORE96, options: list[TransferOptions]) -> float:
        return 0
