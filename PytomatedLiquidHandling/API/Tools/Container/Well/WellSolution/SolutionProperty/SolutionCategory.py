from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .HomogeneitySolutionProperty import HomogeneitySolutionProperty
from .LLDSolutionProperty import LLDSolutionProperty
from .ViscositySolutionProperty import ViscositySolutionProperty
from .VolatilitySolutionProperty import VolatilitySolutionProperty


@dataclass
class SolutionCategory(UniqueObjectABC):
    UniqueIdentifier: str = field(init=False)
    VolatilityProperty: VolatilitySolutionProperty
    ViscosityProperty: ViscositySolutionProperty
    HomogeneityProperty: HomogeneitySolutionProperty
    LLDProperty: LLDSolutionProperty

    def __post_init__(self):
        self.VolatilityProperty.name
        self.UniqueIdentifier = (
            "Volatility"
            + self.VolatilityProperty.name
            + "Viscosity"
            + self.ViscosityProperty.name
            + "Homogeneity"
            + self.HomogeneityProperty.name
            + "LLD"
            + self.LLDProperty.name
        ).replace(" ", "")

    def GetMinAspirateMixParam(self):
        ReturnMinMixParam = 0

        MinMixParam = self.VolatilityProperty.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.ViscosityProperty.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.HomogeneityProperty.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.LLDProperty.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        return ReturnMinMixParam

    def GetMinDispenseMixParam(self):
        ReturnMinMixParam = 0

        MinMixParam = self.VolatilityProperty.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.ViscosityProperty.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.HomogeneityProperty.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.LLDProperty.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        return ReturnMinMixParam
