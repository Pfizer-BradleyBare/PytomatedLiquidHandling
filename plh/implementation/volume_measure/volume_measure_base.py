from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import carrier_location, labware, layout_item
from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True)
class MeasureValues:
    volume: float
    height: float


@dataclasses.dataclass(kw_only=True, eq=False)
class VolumeMeasureBase(Resource):
    """Device that can be used to measure the volume of liquid in a container."""

    supported_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ]
    supported_carrier_locations: Annotated[
        list[carrier_location.CarrierLocationBase],
        BeforeValidator(carrier_location.validate_list),
    ]

    def assert_supported_labware(
        self: VolumeMeasureBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_carrier_locations(
        self: VolumeMeasureBase,
        *args: carrier_location.CarrierLocationBase,
    ) -> None:
        exceptions = [
            carrier_location.exceptions.CarrierLocationNotSupportedError(self, item)
            for item in args
            if item not in self.supported_carrier_locations
        ]

        if len(exceptions) != 0:
            msg = "Some deck locations are not supported."
            raise ExceptionGroup(msg, exceptions)

    @abstractmethod
    def measure(
        self: VolumeMeasureBase,
        *args: tuple[layout_item.LayoutItemBase, int | str],
    ) -> list[MeasureValues]:
        """Measures container and returns a list of MeasureValues."""
