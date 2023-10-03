from dataclasses import dataclass, field

from .Homogeneity import Homogeneity
from .LLD import LLD
from .Viscosity import Viscosity
from .Volatility import Volatility


@dataclass
class Properties:
    Name: str = field(init=False)
    Volatility: Volatility
    Viscosity: Viscosity
    Homogeneity: Homogeneity
    LLD: LLD

    def __post_init__(self):
        self.Name = (
            "Volatility"
            + self.Volatility.name
            + "Viscosity"
            + self.Viscosity.name
            + "Homogeneity"
            + self.Homogeneity.name
            + "LLD"
            + self.LLD.name
        ).replace(" ", "")

    def GetMinAspirateMixParam(self):
        ReturnMinMixParam = 0

        MinMixParam = self.Volatility.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.Viscosity.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.Homogeneity.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.LLD.value.MinAspirateMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        return ReturnMinMixParam

    def GetMinDispenseMixParam(self):
        ReturnMinMixParam = 0

        MinMixParam = self.Volatility.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.Viscosity.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.Homogeneity.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.LLD.value.MinDispenseMix
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        return ReturnMinMixParam
