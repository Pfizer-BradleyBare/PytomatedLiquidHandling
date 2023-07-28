import copy
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .WellSolution import WellSolutionTracker
from .WellSolution.SolutionProperty import (
    HomogeneitySolutionProperty,
    LLDSolutionProperty,
    SolutionCategory,
    ViscositySolutionProperty,
    VolatilitySolutionProperty,
)


@dataclass
class Well(UniqueObjectABC, WellSolutionTracker):
    UniqueIdentifier: int
    LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem | None = field(
        init=True, default=None
    )

    def Aspirate(self, Volume: float) -> WellSolutionTracker:
        WellSolutionTrackerInstance = WellSolutionTracker()

        TotalVolume = sum(
            [WellSolution.Volume for WellSolution in self.GetObjectsAsList()]
        )

        if Volume > TotalVolume:
            raise Exception(
                "You are removing more liquid than is available in the wells. This is weird."
            )

        FractionRemoved = Volume / TotalVolume

        for WellSolutionInstance in self.GetObjectsAsList():
            RemovedVolume = WellSolutionInstance.Volume * FractionRemoved
            NewVolume = WellSolutionInstance.Volume - RemovedVolume

            RemovedWellSolutionInstance = copy.copy(
                WellSolutionInstance
            )  # use a shallow copy to preserve all references.
            RemovedWellSolutionInstance.Volume = RemovedVolume
            WellSolutionTrackerInstance.LoadSingle(RemovedWellSolutionInstance)

            WellSolutionInstance.Volume = NewVolume

            if NewVolume == 0:
                self.UnloadSingle(WellSolutionInstance)

        return WellSolutionTrackerInstance

    def Dispense(self, WellSolutionTrackerInstance: WellSolutionTracker):
        for WellSolutionInstance in WellSolutionTrackerInstance.GetObjectsAsList():
            if self.IsTracked(WellSolutionInstance.UniqueIdentifier):
                self.GetObjectByName(
                    WellSolutionInstance.UniqueIdentifier
                ).Volume += WellSolutionInstance.Volume

            else:
                self.LoadSingle(WellSolutionInstance)

    def GetLiquidClassCategory(self) -> SolutionCategory:
        WellSolutionInstances = self.GetObjectsAsList()

        WellVolume = sum(WellSolution.Volume for WellSolution in WellSolutionInstances)
        # A solution will technically not have a well volume because we never pipette into a solution. Only out of

        VolatilityList = list()
        ViscosityList = list()
        HomogeneityList = list()
        LLDList = list()

        for WellSolutionInstance in WellSolutionInstances:
            Percentage = int(WellSolutionInstance.Volume * 100 / WellVolume)

            SolutionCategoryInstance = WellSolutionInstance.SolutionCategoryInstance

            VolatilityList += (
                [SolutionCategoryInstance.VolatilityProperty.value.NumericValue]
                * Percentage
                * SolutionCategoryInstance.VolatilityProperty.value.Weight
            )

            ViscosityList += (
                [SolutionCategoryInstance.ViscosityProperty.value.NumericValue]
                * Percentage
                * SolutionCategoryInstance.ViscosityProperty.value.Weight
            )

            HomogeneityList += (
                [SolutionCategoryInstance.HomogeneityProperty.value.NumericValue]
                * Percentage
                * SolutionCategoryInstance.HomogeneityProperty.value.Weight
            )

            LLDList += (
                [SolutionCategoryInstance.LLDProperty.value.NumericValue]
                * Percentage
                * SolutionCategoryInstance.LLDProperty.value.Weight
            )

        Volatility = VolatilitySolutionProperty.GetByNumericKey(
            int(round(sum(VolatilityList) / len(VolatilityList)))
        )

        Viscosity = ViscositySolutionProperty.GetByNumericKey(
            int(round(sum(ViscosityList) / len(ViscosityList)))
        )

        Homogeneity = HomogeneitySolutionProperty.GetByNumericKey(
            int(round(sum(HomogeneityList) / len(HomogeneityList)))
        )

        LLD = LLDSolutionProperty.GetByNumericKey(
            int(round(sum(LLDList) / len(LLDList)))
        )
        # We are going to process the whole shebang here

        return SolutionCategory(Volatility, Viscosity, Homogeneity, LLD)
