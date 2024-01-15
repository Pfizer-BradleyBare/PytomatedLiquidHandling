from pydantic import dataclasses

from .Base import CarrierABC


@dataclasses.dataclass(kw_only=True)
class NonMoveableCarrier(CarrierABC):
    """A carrier which can not be moved in any way."""
