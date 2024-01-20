from __future__ import annotations

from dataclasses import field
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uLCOREGrip
from plh.hal import deck_location, layout_item

from .transport_base import *
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True)
class HamiltonCOREGripper(TransportBase):
    backend: HamiltonBackendBase
    gripper_labware_id: str

    @dataclasses.dataclass(kw_only=True)
    class PickupOptions(TransportBase.PickupOptions):
        """Options to pick up labware from deck location"""

    @dataclasses.dataclass(kw_only=True)
    class DropoffOptions(TransportBase.DropoffOptions):
        """Options to drop off labware to deck location"""

        CheckPlateExists: Channel1000uLCOREGrip.PlacePlate.YesNoOptions = field(
            compare=False,
        )

    def transport(
        self: HamiltonCOREGripper,
        source_layout_item: layout_item.LayoutItemBase,
        destination_layout_item: layout_item.LayoutItemBase,
    ) -> None:
        if source_layout_item.deck_location == destination_layout_item.deck_location:
            return

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source_layout_item.deck_location,
                destination_layout_item.deck_location,
            )[0]
        )

        labware = source_layout_item.labware

        get_plate_options = Channel1000uLCOREGrip.GetPlate.Options(
            GripperLabwareID=self.gripper_labware_id,
            PlateLabwareID=source_layout_item.labware_id,
            GripWidth=labware.dimensions.y_length - labware.transport_offsets.close,
            OpenWidth=labware.dimensions.y_length + labware.transport_offsets.open,
            GripHeight=labware.transport_offsets.top,
        )

        command = Channel1000uLCOREGrip.GetPlate.Command(
            options=get_plate_options,
            backend_error_handling=False,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            Channel1000uLCOREGrip.GetPlate.Response,
        )

        dropoff_options = cast(
            HamiltonCOREGripper.DropoffOptions,
            compatible_configs[1].dropoff_options,
        )

        command = Channel1000uLCOREGrip.PlacePlate.Command(
            options=Channel1000uLCOREGrip.PlacePlate.Options(
                LabwareID=destination_layout_item.labware_id,
                CheckPlateExists=dropoff_options.CheckPlateExists,
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

    def transport_time(
        self: HamiltonCOREGripper,
        source_layout_item: layout_item.LayoutItemBase,
        destination_layout_item: layout_item.LayoutItemBase,
    ) -> float:
        ...
