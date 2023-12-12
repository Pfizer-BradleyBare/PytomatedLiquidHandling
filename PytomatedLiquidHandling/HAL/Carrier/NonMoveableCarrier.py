from .Base import CarrierABC

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class NonMoveableCarrier(CarrierABC):
    """A carrier which can not be moved in any way."""
