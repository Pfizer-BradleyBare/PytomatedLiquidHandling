from pydantic import field_validator
from pydantic.dataclasses import dataclass

from PytomatedLiquidHandling.HAL import Carrier, GetCarriers


@dataclass
class CarrierConfig:
    Carrier: Carrier.Base.CarrierABC
    CarrierPosition: int

    @field_validator("Carrier")
    def CarrierValidate(cls, v):
        if v not in GetCarriers():
            raise ValueError(
                v + " not found in Carriers. Did you disable or forget to add it?"
            )

        return GetCarriers()[v]
