from pydantic import BaseModel, field_validator

from PytomatedLiquidHandling.HAL import LayoutItem


class DefaultVacuumPressures(BaseModel):
    Low: float
    Medium: float
    High: float


class FilterPlateConfiguration(BaseModel):
    FilterPlateStack: LayoutItem.FilterPlateStack
    CollectionPlate: LayoutItem.Plate
    DefaultVacuumPressures: DefaultVacuumPressures

    @field_validator("FilterPlateStack", "CollectionPlate", mode="before")
    def __PlatesValidate(cls, v):
        Identifier = v

        Objects = LayoutItem.Devices

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + LayoutItem.Base.LayoutItemABC.__name__
                + " objects."
            )

        return Objects[Identifier]
