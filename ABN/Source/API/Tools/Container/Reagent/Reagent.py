from ..BaseContainer.Container import Container
from ..BaseContainer.LiquidClassCategory.LiquidClassCategory import LiquidClassCategory
from ..Plate.Well.WellSolution.WellSolution import WellSolution
from ..Plate.Well.WellSolution.WellSolutionTracker import WellSolutionTracker
from .ReagentProperty import (
    HomogeneityReagentProperty,
    LLDReagentProperty,
    ViscosityReagentProperty,
    VolatilityReagentProperty,
)


class Reagent(Container):
    def __init__(
        self,
        Name: str,
        MethodName: str,
        Volatility: VolatilityReagentProperty,
        Viscosity: ViscosityReagentProperty,
        Homogeneity: HomogeneityReagentProperty,
        LLD: LLDReagentProperty,
    ):
        Container.__init__(self, Name, MethodName, "No Preference")

        self.Volatility: VolatilityReagentProperty = Volatility
        self.Viscosity: ViscosityReagentProperty = Viscosity
        self.Homogeneity: HomogeneityReagentProperty = Homogeneity
        self.LLD: LLDReagentProperty = LLD

        self.UsedVolume = 0

    def GetVolume(self) -> float:
        return self.UsedVolume

    def GetLiquidClassCategory(self) -> LiquidClassCategory:
        return LiquidClassCategory(
            self.Volatility, self.Viscosity, self.Homogeneity, self.LLD
        )

    def Aspirate(self, WellNumber: int, Volume: float) -> WellSolutionTracker:
        self.UsedVolume -= Volume

        ReturnWellSolutionTrackerInstance = WellSolutionTracker()
        ReturnWellSolutionTrackerInstance.ManualLoad(
            WellSolution(self.GetName(), Volume)
        )

        return ReturnWellSolutionTrackerInstance

    def Dispense(
        self, WellNumber: int, WellSolutionTrackerInstance: WellSolutionTracker
    ):
        raise Exception(
            "It is not possible to dispense into a reagent container. Sorry!"
        )
