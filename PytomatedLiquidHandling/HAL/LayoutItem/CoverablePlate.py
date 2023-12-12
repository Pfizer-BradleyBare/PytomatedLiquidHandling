from pydantic import Field, field_validator

from PytomatedLiquidHandling.HAL import Labware, LayoutItem

from .Base import LayoutItemABC
from .Lid import Lid

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class CoverablePlate(LayoutItemABC):
    Labware: Labware.PipettableLabware
    Lid: Lid
    IsCovered: bool = Field(exclude=True, default=False)

    @field_validator("Lid", mode="before")
    def __LidValidate(cls, v):
        Objects = LayoutItem.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + LayoutItem.Base.LayoutItemABC.__name__
                + " objects."
            )

        return Objects[Identifier]
