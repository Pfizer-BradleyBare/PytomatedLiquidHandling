from pydantic import BaseModel

from PytomatedLiquidHandling.HAL import LayoutItem


class DefaultVacuumPressures(BaseModel):
    Low: float
    Medium: float
    High: float


class FilterPlateConfiguration(BaseModel):
    FilterPlateStack: LayoutItem.FilterPlateStack
    CollectionPlate: LayoutItem.Plate
    DefaultVacuumPressures: DefaultVacuumPressures
