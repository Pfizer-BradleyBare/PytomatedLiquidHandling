from pydantic import dataclasses

from .Base import CarrierABC


@dataclasses.dataclass(kw_only=True)
class MoveableCarrier(CarrierABC):
    """A carrier which can be accessed and moved manually."""
