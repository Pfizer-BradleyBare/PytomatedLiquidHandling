from __future__ import annotations

from dataclasses import field
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uLCOREGrip
from plh.hal import deck_location

from .transport_base import *
from .transport_base import TransportBase, TransportOptions


@dataclasses.dataclass(kw_only=True)
class HamiltonCOREGripper(TransportBase):
    backend: HamiltonBackendBase
    gripper_labware_id: str

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions):
        """Options to pick up labware from deck location"""

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        """Options to drop off labware to deck location"""

        CheckPlateExists: Channel1000uLCOREGrip.PlacePlate.YesNoOptions = field(
            compare=False,
        )

    def get(
        self: HamiltonCOREGripper,
        options: TransportOptions,
    ) -> None:
        source_layout_item = options.SourceLayoutItem

        labware = source_layout_item.labware

        command = Channel1000uLCOREGrip.GetPlate.Command(
            options=Channel1000uLCOREGrip.GetPlate.Options(
                GripperLabwareID=self.gripper_labware_id,
                PlateLabwareID=source_layout_item.labware_id,
                GripWidth=labware.dimensions.y_length - labware.transport_offsets.close,
                OpenWidth=labware.dimensions.y_length + labware.transport_offsets.open,
                GripHeight=labware.transport_offsets.top,
            ),
            backend_error_handling=False,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            Channel1000uLCOREGrip.GetPlate.Response,
        )

    def get_time(
        self: HamiltonCOREGripper,
        options: TransportOptions,
    ) -> float:
        ...

    def place(
        self: HamiltonCOREGripper,
        options: TransportOptions,
    ) -> None:
        source_layout_item = options.SourceLayoutItem
        destination_layout_item = options.DestinationLayoutItem

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source_layout_item.deck_location,
                destination_layout_item.deck_location,
            )[0]
        )

        place_options = cast(
            HamiltonCOREGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = Channel1000uLCOREGrip.PlacePlate.Command(
            options=Channel1000uLCOREGrip.PlacePlate.Options(
                LabwareID=destination_layout_item.labware_id,
                CheckPlateExists=place_options.CheckPlateExists,
                EjectTool=Channel1000uLCOREGrip.PlacePlate.YesNoOptions(
                    int(self._last_transport_flag),
                ),
            ),
            backend_error_handling=False,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            Channel1000uLCOREGrip.PlacePlate.Response,
        )

    def place_time(
        self: HamiltonCOREGripper,
        options: TransportOptions,
    ) -> float:
        ...
