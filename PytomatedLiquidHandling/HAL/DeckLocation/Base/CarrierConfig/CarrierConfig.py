from pydantic import BaseModel, field_validator

from PytomatedLiquidHandling.HAL import Carrier


class CarrierConfig(BaseModel):
    Carrier: Carrier.Base.CarrierABC
    Position: int

    @field_validator("Carrier", mode="before")
    def __CarrierValidate(cls, v):
        Objects = Carrier.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Carrier.Base.CarrierABC.__name__
                + " objects."
            )

        return Objects[Identifier]
