from pydantic import dataclasses, model_validator

from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from .CarrierConfig import CarrierConfig


@dataclasses.dataclass(kw_only=True)
class DeckLocationABC(HALDevice):
    """A specific location on an automation deck.

    Attributes:
        CarrierConfig: See DeckLocation.Base.CarrierConfig class.
    """

    Identifier: str = "None"

    CarrierConfig: CarrierConfig

    @model_validator(mode="after")
    def __ModelValidate(cls, v):
        if v.Identifier == "None":
            v.Identifier = f"{v.CarrierConfig.Carrier.Identifier}_Pos{str(v.CarrierConfig.Position)}"
        return v