from __future__ import annotations

from dataclasses import dataclass

from plh.implementation.exceptions import HALError

from .carrier_location_base import CarrierLocationBase


@dataclass
class CarrierLocationNotSupportedError(HALError):
    """HAL device does not support your CarrierLocation.
    This can be thrown for any LayoutItem inputs.
    """

    carrier_location: CarrierLocationBase
    """CarrierLocationBase object that is not supported."""

    def __str__(self) -> str:
        return self.carrier_location.identifier


@dataclass
class CarrierLocationNotTransportableError(HALError):
    """Your deck location is not transportable but the action you attempted requires a transportable deck location."""

    carrier_location: CarrierLocationBase
    """CarrierLocationBase object that is not transportable."""

    def __str__(self) -> str:
        return self.carrier_location.identifier


@dataclass
class CarrierLocationTransportConfigsNotCompatibleError(HALError):
    """The two transportable deck locations do not have compatible transport options.
    Thus, you cannot transport to/from these deck locations.
    You should find an intermediate deck location to enable comaptibility.
    """

    source_carrier_location: CarrierLocationBase
    """Source transportable deck location."""

    destination_carrier_location: CarrierLocationBase
    """Destination transportable deck location."""

    def __str__(self) -> str:
        return f"{self.source_carrier_location.identifier} != {self.destination_carrier_location.identifier}"