from typing import cast

from pydantic import ValidationInfo, dataclasses, field_validator

from PytomatedLiquidHandling.HAL import Carrier

_UsedCarriers: list[str] = list()


@dataclasses.dataclass(kw_only=True)
class CarrierConfig:
    """Connects a DeckLocation to a specific carrier position.

    Attributes:
        Carrier: A carrier device.
        Position: A position on that carrier.
    """

    Carrier: Carrier.Base.CarrierABC
    Position: int

    @field_validator(
        "Carrier",
        mode="before",
    )
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

    @field_validator("Position", mode="after")
    def __PositionValidate(cls, v, Info: ValidationInfo):
        try:
            AssignedCarrier = cast(Carrier.Base.CarrierABC, Info.data["Carrier"])
        except KeyError:
            return v

        NumPositions = AssignedCarrier.NumLabwarePositions

        if v > NumPositions:
            raise ValueError(
                f"Carrier position ({str(v)}) must be less than total number of supported labware positions ({str(NumPositions)})."
            )

        CarrierPosID = AssignedCarrier.Identifier + str(v)

        global _UsedCarriers

        if CarrierPosID in _UsedCarriers:
            raise ValueError(
                f'Position {str(v)} has already been assigned on carrier "{AssignedCarrier.Identifier}".'
            )

        _UsedCarriers.append(CarrierPosID)

        return v
