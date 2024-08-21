from __future__ import annotations

from typing import cast

from pydantic import dataclasses

from plh.device.tools import *

from .carrier_location_base import *
from .carrier_location_base import CarrierLocationBase
from .transport_config import *
from .transport_config import TransportConfig


@dataclasses.dataclass(kw_only=True, eq=False)
class TransportableCarrierLocation(CarrierLocationBase):
    """A specific location on an automation deck that can be transported to/from."""

    transport_configs: list[TransportConfig]
    """A list of possible ways to transport to/from this deck location."""

    @classmethod
    def get_compatible_transport_configs(
        cls: type[TransportableCarrierLocation],
        source: CarrierLocationBase,
        destination: CarrierLocationBase,
    ) -> list[tuple[TransportConfig, TransportConfig]]:
        """Gets a list of compatible transport configurations for different deck locations.

        If CarrierLocationNotTransportableError is thrown then your deck location is not compatible with transport.
        """
        if not all(
            isinstance(location, TransportableCarrierLocation)
            for location in [source, destination]
        ):
            return []

        return [
            (source_config, destination_config)
            for source_config in cast(
                TransportableCarrierLocation,
                source,
            ).transport_configs
            for destination_config in cast(
                TransportableCarrierLocation,
                destination,
            ).transport_configs
            if source_config == destination_config
        ]
        # __eq__ is defined for transport config so we just iterate through and collect the ones that are equal.
