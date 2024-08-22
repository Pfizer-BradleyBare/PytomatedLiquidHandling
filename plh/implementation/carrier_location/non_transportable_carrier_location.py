from __future__ import annotations

from pydantic import dataclasses

from .carrier_location_base import CarrierLocationBase


@dataclasses.dataclass(kw_only=True, eq=False)
class NonTransportableCarrierLocation(CarrierLocationBase):
    """A specific location on an automation deck that cannot be transported to/from."""
