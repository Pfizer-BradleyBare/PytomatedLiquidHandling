from ......Tools.AbstractClasses import UniqueObjectABC
from ...Reagent.ReagentProperty import (
    HomogeneityReagentProperty,
    LLDReagentProperty,
    ViscosityReagentProperty,
    VolatilityReagentProperty,
)


class LiquidClassCategory(UniqueObjectABC):
    def __init__(
        self,
        Volatility: VolatilityReagentProperty,
        Viscosity: ViscosityReagentProperty,
        Homogeneity: HomogeneityReagentProperty,
        LLD: LLDReagentProperty,
    ):
        self.Volatility: VolatilityReagentProperty = Volatility
        self.Viscosity: ViscosityReagentProperty = Viscosity
        self.Homogeneity: HomogeneityReagentProperty = Homogeneity
        self.LLD: LLDReagentProperty = LLD

    def GetUniqueIdentifier(self) -> str:
        return (
            "Volatility"
            + self.Volatility.name
            + "Viscosity"
            + self.Viscosity.name
            + "Homogeneity"
            + self.Homogeneity.name
            + "LLD"
            + self.LLD.name
        ).replace(" ", "")

    def GetVolatility(self) -> VolatilityReagentProperty:
        return self.Volatility

    def GetViscosity(self) -> ViscosityReagentProperty:
        return self.Viscosity

    def GetHomogeneity(self) -> HomogeneityReagentProperty:
        return self.Homogeneity

    def GetLLD(self) -> LLDReagentProperty:
        return self.LLD

    def GetMinAspirateMixParam(self):
        ReturnMinMixParam = 0

        MinMixParam = self.GetVolatility().value.GetMinAspirateMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.GetViscosity().value.GetMinAspirateMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.GetHomogeneity().value.GetMinAspirateMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.GetLLD().value.GetMinAspirateMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        return ReturnMinMixParam

    def GetMinDispenseMixParam(self):
        ReturnMinMixParam = 0

        MinMixParam = self.GetVolatility().value.GetMinDispenseMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.GetViscosity().value.GetMinDispenseMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.GetHomogeneity().value.GetMinDispenseMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        MinMixParam = self.GetLLD().value.GetMinDispenseMix()
        if MinMixParam > ReturnMinMixParam:
            ReturnMinMixParam = MinMixParam

        return ReturnMinMixParam
