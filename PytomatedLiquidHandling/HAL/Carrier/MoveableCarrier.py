from .Base import CarrierABC

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class MoveableCarrier(CarrierABC):
    """A carrier which can be accessed and moved manually."""
