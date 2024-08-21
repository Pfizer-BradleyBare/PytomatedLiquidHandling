from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware
from plh.implementation import layout_item as li
from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class HeatCoolShakeBase(Resource):
    """A device that can perform either heating, cooling, and shaking or any combination of the three."""

    plates: Annotated[
        list[li.CoverablePlate | li.Plate],
        BeforeValidator(li.validate_list),
    ]
    """Plates where incubations, shaking will occur."""

    def assert_supported_labware(
        self: HeatCoolShakeBase,
        *args: labware.LabwareBase,
    ) -> None:
        supported_labware = [item.labware for item in self.plates]

        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def get_layout_item(
        self: HeatCoolShakeBase,
        labware: labware.LabwareBase,
    ) -> li.CoverablePlate | li.Plate:
        """Gets a layout item on the heat_cool_shake device that is compatible with your current layout item."""
        self.assert_supported_labware(labware)

        for supported_layout_item in self.plates:
            if supported_layout_item.labware == labware:
                return supported_layout_item

        msg = "Should never reach this point."
        raise RuntimeError(msg)

    @abstractmethod
    def assert_temperature(self, temperature: float) -> None: ...

    @abstractmethod
    def set_temperature(self: HeatCoolShakeBase, temperature: float) -> None:
        """Sets temperature on the device."""
        ...

    @abstractmethod
    def set_temperature_time(
        self: HeatCoolShakeBase,
        temperature: float,
    ) -> float:
        """Calculates the time to cool or heat to your desired temperature."""
        ...

    @abstractmethod
    def get_temperature(self: HeatCoolShakeBase) -> float:
        """Gets the current temperature."""
        ...

    @abstractmethod
    def assert_rpm(
        self: HeatCoolShakeBase,
        rpm: float,
    ) -> None: ...

    @abstractmethod
    def set_shaking_speed(
        self: HeatCoolShakeBase,
        rpm: float,
    ) -> None:
        """Sets the shaking speed on your device. NOTE: To turn off shaking set the speed to 0."""
        ...

    @abstractmethod
    def get_shaking_speed(self: HeatCoolShakeBase) -> int:
        """Get current shaking speed."""
        ...
