from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses, field_validator

from plh.hal import carrier
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True, eq=False)
class CarrierLoaderBase(HALDevice, Interface):
    """A device that can move a carrier in and out of a system without user intervention."""

    supported_carriers: list[carrier.CarrierBase]

    @field_validator("supported_carriers", mode="before")
    @classmethod
    def __supported_carriers_validate(
        cls: type[CarrierLoaderBase],
        v: list[str | carrier.CarrierBase],
    ) -> list[carrier.CarrierBase]:
        supported_objects = []

        objects = carrier.devices

        for item in v:
            if isinstance(item, carrier.CarrierBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + carrier.CarrierBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    @abstractmethod
    def load(
        self: CarrierLoaderBase,
        carrier: carrier.CarrierBase,
    ) -> list[tuple[int, str]]:
        """Move carrier into the deck."""

    @abstractmethod
    def unload(self: CarrierLoaderBase, carrier: carrier.CarrierBase) -> None:
        """Move carrier out from the deck."""
