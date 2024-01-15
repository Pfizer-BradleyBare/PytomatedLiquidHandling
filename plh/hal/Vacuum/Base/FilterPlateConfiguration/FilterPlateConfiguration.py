from pydantic import dataclasses, field_validator

from plh.hal import LayoutItem


@dataclasses.dataclass(kw_only=True)
class DefaultVacuumPressures:
    Low: float
    Medium: float
    High: float


from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class FilterPlateConfiguration:
    FilterPlate: LayoutItem.FilterPlate | LayoutItem.CoverableFilterPlate
    CollectionPlate: LayoutItem.Plate
    MaxPressure: float
    DefaultVacuumPressures: DefaultVacuumPressures

    @field_validator("FilterPlateStack", "CollectionPlate", mode="before")
    def __PlatesValidate(cls, v):
        Identifier = v

        Objects = LayoutItem.Devices

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + LayoutItem.Base.LayoutItemBase.__name__
                + " objects.",
            )

        return Objects[Identifier]
