from pydantic.dataclasses import dataclass
from pydantic import validator

from PytomatedLiquidHandling.HAL import Carrier, Carriers


@dataclass
class CarrierConfig:
    Carrier: Carrier.Base.CarrierABC
    CarrierPosition: int

    @validator("Carrier")
    def CarrierValidate(cls, Carrier):
        if Carrier not in Carriers:
            raise ValueError(
                Carrier + " not found in Carriers. Did you disable or forget to add it?"
            )

        return Carriers[Carrier]
