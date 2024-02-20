from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import labware
from plh.hal import layout_item as li
from plh.hal.tools import HALDevice, Interface

from .options import HeatCoolShakeOptions


@dataclasses.dataclass(kw_only=True, eq=False)
class HeatCoolShakeBase(Interface, HALDevice):
    """A device that can perform either heating, cooling, and shaking or any combination of the three."""

    plates: Annotated[
        list[li.CoverablePlate | li.Plate],
        BeforeValidator(li.validate_list),
    ]
    """Plates where incubations, shaking will occur."""

    def assert_get_layout_item(
        self: HeatCoolShakeBase,
        options: HeatCoolShakeOptions,
    ) -> None:
        """Must called before calling ```get_layout_item```.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ValueError or ExceptionGroup of the following:
            Labware.LabwareNotSupportedError
        """
        if options.layout_item is None:
            raise ValueError("layout_item must not be None")

        excepts = []

        layout_item = options.layout_item

        supported_labware = [
            layout_item.labware.identifier for layout_item in self.plates
        ]

        if layout_item.labware not in supported_labware:
            excepts.append(
                labware.exceptions.LabwareNotSupportedError(
                    self,
                    layout_item.labware,
                ),
            )

        if len(excepts) > 0:
            msg = "Exceptions"
            raise ExceptionGroup(msg, excepts)

    def get_layout_item(
        self: HeatCoolShakeBase,
        options: HeatCoolShakeOptions,
    ) -> li.CoverablePlate | li.Plate:
        """Gets a layout item on the heat_cool_shake device that is compatible with your current layout item."""
        self.assert_get_layout_item(options)

        layout_item = options.layout_item

        assert layout_item is not None

        for supported_layout_item in self.plates:
            if supported_layout_item.labware == layout_item.labware:
                return supported_layout_item

        raise labware.exceptions.LabwareNotSupportedError(self, layout_item.labware)

    @abstractmethod
    def assert_set_temperature(
        self: HeatCoolShakeBase,
        options: HeatCoolShakeOptions,
    ) -> None:
        """Must called before calling ```set_temperature``` and ```set_temperature_time```.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ValueError or ExceptionGroup of the following:

            HeatCoolShakeDevice.CoolingNotSupportedError

            HeatCoolShakeDevice.HeatingNotSupportedError
        """
        if options.temperature is None:
            raise ValueError("temperature must not be None")

    @abstractmethod
    def set_temperature(self: HeatCoolShakeBase, options: HeatCoolShakeOptions) -> None:
        """Sets temperature on the device."""
        ...

    @abstractmethod
    def set_temperature_time(
        self: HeatCoolShakeBase,
        options: HeatCoolShakeOptions,
    ) -> float:
        """Calculates the time to cool or heat to your desired temperature."""
        ...

    @abstractmethod
    def get_temperature(self: HeatCoolShakeBase) -> float:
        """Gets the current temperature."""
        ...

    @abstractmethod
    def assert_set_shaking_speed(
        self: HeatCoolShakeBase,
        options: HeatCoolShakeOptions,
    ) -> None:
        """Must called before calling ```set_shaking_speed```.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ValueError or ExceptionGroup of the following:

            HeatCoolShakeDevice.ShakingNotSupportedError
        """
        if options.rpm is None:
            raise ValueError("rpm must not be None")

    @abstractmethod
    def set_shaking_speed(
        self: HeatCoolShakeBase,
        options: HeatCoolShakeOptions,
    ) -> None:
        """Sets the shaking speed on your device. NOTE: To turn off shaking set the speed to 0."""
        ...

    @abstractmethod
    def get_shaking_speed(self: HeatCoolShakeBase) -> int:
        """Get current shaking speed."""
        ...
