from pydantic import Field, dataclasses, field_validator

from plh.hal import Labware, LayoutItem

from .Base import LayoutItemBase
from .Lid import Lid


@dataclasses.dataclass(kw_only=True)
class CoverablePlate(LayoutItemBase):
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
                + LayoutItem.Base.LayoutItemBase.__name__
                + " objects.",
            )

        return Objects[Identifier]
