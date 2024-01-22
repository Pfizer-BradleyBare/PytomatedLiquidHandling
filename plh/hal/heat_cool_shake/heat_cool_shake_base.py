from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses, field_validator

from plh.hal import labware
from plh.hal import layout_item as li
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class HeatCoolShakeBase(Interface, HALDevice):
    """A device that can perform either heating, cooling, and shaking or any combination of the three."""

    plates: list[li.CoverablePlate | li.Plate]
    """Plates where incubations, shaking will occur."""

    @field_validator("plates", mode="before")
    @classmethod
    def __supported_plates_validate(
        cls: type[HeatCoolShakeBase],
        v: list[str | li.LayoutItemBase],
    ) -> list[li.LayoutItemBase]:
        supported_objects = []

        objects = li.devices

        for item in v:
            if isinstance(item, li.LayoutItemBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + li.LayoutItemBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    def assert_options(
        self: HeatCoolShakeBase,
        layout_item: li.LayoutItemBase | None = None,
        temperature: None | float = None,
        rpm: None | int = None,
    ) -> None:
        """Must called before calling ```get_layout_item```, ```set_temperature```, ```set_temperature_time```, and ```set_shaking_speed```.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ExceptionGroup of the following:

            Labware.LabwareNotSupportedError

            HeatCoolShakeDevice.CoolingNotSupportedError

            HeatCoolShakeDevice.HeatingNotSupportedError

            HeatCoolShakeDevice.ShakingNotSupportedError
        """
        excepts = []

        if layout_item is not None:
            supported_labware = [
                layout_item.labware.identifier for LayoutItem in self.plates
            ]

            if layout_item.labware not in supported_labware:
                excepts.append(
                    labware.LabwareNotSupportedError([layout_item.labware]),
                )

        if len(excepts) > 0:
            msg = "HeatCoolShakeDevice Options Exceptions"
            raise ExceptionGroup(msg, excepts)

    def get_layout_item(
        self: HeatCoolShakeBase,
        layout_item: li.LayoutItemBase,
    ) -> li.CoverablePlate | li.Plate:
        """Gets a layout item on the heat_cool_shake device that is compatible with your current layout item."""

        for supported_layout_item in self.plates:
            if supported_layout_item.labware == layout_item.labware:
                if isinstance(supported_layout_item, li.CoverablePlate):
                    if isinstance(layout_item, li.CoverablePlate):
                        supported_layout_item.is_covered = layout_item.is_covered
                    else:
                        supported_layout_item.is_covered = False

                return supported_layout_item

        raise labware.LabwareNotSupportedError([layout_item.labware])

    @abstractmethod
    def set_temperature(self: HeatCoolShakeBase, temperature: float) -> None:
        """Sets temperature on the device."""
        ...

    @abstractmethod
    def set_temperature_time(self: HeatCoolShakeBase, temperature: float) -> float:
        """Calculates the time to cool or heat to your desired temperature."""
        ...

    @abstractmethod
    def get_temperature(self: HeatCoolShakeBase) -> float:
        """Gets the current temperature."""
        ...

    @abstractmethod
    def set_shaking_speed(self: HeatCoolShakeBase, rpm: int) -> None:
        """Sets the shaking speed on your device. NOTE: To turn off shaking set the speed to 0."""
        ...

    @abstractmethod
    def get_shaking_speed(self: HeatCoolShakeBase) -> int:
        """Get current shaking speed."""
        ...
