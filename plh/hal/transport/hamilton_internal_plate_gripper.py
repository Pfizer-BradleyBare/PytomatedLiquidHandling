from __future__ import annotations

from dataclasses import field
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import iSwap
from plh.hal import deck_location, layout_item

from .transport_base import *
from .transport_base import TransportBase


@dataclasses.dataclass(kw_only=True)
class HamiltonInternalPlateGripper(TransportBase):
    backend: HamiltonBackendBase

    @dataclasses.dataclass(kw_only=True)
    class GetOptions(TransportBase.GetOptions):
        """Options to pick up labware from deck location"""

        GripMode: iSwap.GetPlate.GripModeOptions = field(compare=True)
        Movement: iSwap.GetPlate.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: iSwap.GetPlate.LabwareOrientationOptions = field(
            compare=True,
        )
        InverseGrip: iSwap.GetPlate.YesNoOptions = field(compare=True)

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions(TransportBase.PlaceOptions):
        """Options to drop off labware to deck location"""

        Movement: iSwap.PlacePlate.MovementOptions = field(compare=True)
        RetractDistance: float = field(compare=False)
        LiftupHeight: float = field(compare=False)
        LabwareOrientation: iSwap.PlacePlate.LabwareOrientationOptions = field(
            compare=True,
        )

    def transport(
        self: HamiltonInternalPlateGripper,
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

        get_options = cast(
            HamiltonInternalPlateGripper.GetOptions,
            compatible_configs[0].get_options,
        )

        command = iSwap.GetPlate.Command(
            options=iSwap.GetPlate.Options(
                LabwareID=source_layout_item.labware_id,
                GripWidth=labware.dimensions.y_length - labware.transport_offsets.close,
                OpenWidth=labware.dimensions.y_length + labware.transport_offsets.open,
                GripHeight=labware.transport_offsets.top,
                GripMode=get_options.GripMode,
                Movement=get_options.Movement,
                RetractDistance=get_options.RetractDistance,
                LiftupHeight=get_options.LiftupHeight,
                LabwareOrientation=get_options.LabwareOrientation,
                InverseGrip=get_options.InverseGrip,
            ),
            backend_error_handling=False,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, iSwap.GetPlate.Response)

        place_options = cast(
            HamiltonInternalPlateGripper.PlaceOptions,
            compatible_configs[1].place_options,
        )

        command = iSwap.PlacePlate.Command(
            options=iSwap.PlacePlate.Options(
                LabwareID=destination_layout_item.labware_id,
                Movement=place_options.Movement,
                RetractDistance=place_options.RetractDistance,
                LiftupHeight=place_options.LiftupHeight,
                LabwareOrientation=place_options.LabwareOrientation,
            ),
            backend_error_handling=False,
        )
        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, iSwap.PlacePlate.Response)

    def transport_time(
        self: HamiltonInternalPlateGripper,
        source_layout_item: layout_item.LayoutItemBase,
        destination_layout_item: layout_item.LayoutItemBase,
    ) -> float:
        ...
