from ..BaseContainer.Container import Container
from ..BaseContainer.LiquidClassCategory.LiquidClassCategory import LiquidClassCategory
from ..Plate.Well.WellSolution.WellSolution import WellSolution
from ..Plate.Well.WellSolution.WellSolutionTracker import WellSolutionTracker
from ..Reagent.ReagentProperty import (
    HomogeneityReagentProperty,
    LLDReagentProperty,
    ViscosityReagentProperty,
    VolatilityReagentProperty,
)
from ..Reagent.ReagentTracker import ReagentTracker
from .Well.Well import Well
from .Well.WellTracker import WellTracker


class Plate(Container):
    def __init__(self, Name: str, MethodName: str, Filter: str):
        Container.__init__(self, Name, MethodName, Filter)

        # What solutions and volume is in each well
        self.WellTrackerInstance: WellTracker = WellTracker()

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance

    def GetMaxWellVolume(self) -> float:
        MaxVol = 0

        for WellInstance in self.WellTrackerInstance.GetObjectsAsList():
            if WellInstance.MaxWellVolume > MaxVol:
                MaxVol = WellInstance.MaxWellVolume

        return MaxVol

    def GetMinWellVolume(self) -> float:
        MinVol = 0

        for WellInstance in self.WellTrackerInstance.GetObjectsAsList():
            if WellInstance.MinWellVolume < MinVol:
                MinVol = WellInstance.MinWellVolume

        return MinVol

    def GetVolume(self) -> float:
        return max(self.GetMaxWellVolume(), abs(self.GetMinWellVolume()))

    def GetLiquidClassCategory(
        self, WellNumber: int, ReagentTrackerInstance: ReagentTracker
    ) -> LiquidClassCategory:
        WellInstance = self.GetWellTracker().GetObjectByName(WellNumber)

        WellSolutionInstances = WellInstance.GetWellSolutionTracker().GetObjectsAsList()

        WellVolume = sum(Solution.GetVolume() for Solution in WellSolutionInstances)
        # A solution will technically not have a well volume because we never pipette into a solution. Only out of

        VolatilityList = list()
        ViscosityList = list()
        HomogeneityList = list()
        LLDList = list()

        for WellSolutionInstance in WellSolutionInstances:
            Percentage = int(WellSolutionInstance.GetVolume() * 100 / WellVolume)

            SolutionLiquidClassCategoryInstance = (
                ReagentTrackerInstance.GetObjectByName(
                    WellSolutionInstance.GetName()
                ).GetLiquidClassCategory()
            )

            VolatilityList += (
                [
                    SolutionLiquidClassCategoryInstance.GetVolatility().value.GetNumericValue()
                ]
                * Percentage
                * SolutionLiquidClassCategoryInstance.GetVolatility().value.GetWeight()
            )

            ViscosityList += (
                [
                    SolutionLiquidClassCategoryInstance.GetViscosity().value.GetNumericValue()
                ]
                * Percentage
                * SolutionLiquidClassCategoryInstance.GetViscosity().value.GetWeight()
            )

            HomogeneityList += (
                [
                    SolutionLiquidClassCategoryInstance.GetHomogeneity().value.GetNumericValue()
                ]
                * Percentage
                * SolutionLiquidClassCategoryInstance.GetHomogeneity().value.GetWeight()
            )

            LLDList += (
                [SolutionLiquidClassCategoryInstance.GetLLD().value.GetNumericValue()]
                * Percentage
                * SolutionLiquidClassCategoryInstance.GetLLD().value.GetWeight()
            )

        Volatility = VolatilityReagentProperty.GetByNumericKey(
            int(round(sum(VolatilityList) / len(VolatilityList)))
        )

        Viscosity = ViscosityReagentProperty.GetByNumericKey(
            int(round(sum(ViscosityList) / len(ViscosityList)))
        )

        Homogeneity = HomogeneityReagentProperty.GetByNumericKey(
            int(round(sum(HomogeneityList) / len(HomogeneityList)))
        )

        LLD = LLDReagentProperty.GetByNumericKey(
            int(round(sum(LLDList) / len(LLDList)))
        )
        # We are going to process the whole shebang here

        return LiquidClassCategory(Volatility, Viscosity, Homogeneity, LLD)

    def Aspirate(self, WellNumber: int, Volume: float) -> WellSolutionTracker:

        if not self.GetWellTracker().IsTracked(WellNumber):
            self.GetWellTracker().ManualLoad(Well(WellNumber))
        # If it doesn't exist then lets add it

        SourceWellSolutionTrackerInstance = (
            self.GetWellTracker().GetObjectByName(WellNumber).GetWellSolutionTracker()
        )

        WellVolume = sum(
            Solution.GetVolume()
            for Solution in SourceWellSolutionTrackerInstance.GetObjectsAsList()
        )

        if WellVolume != 0:
            if Volume > WellVolume:
                raise Exception(
                    "You are removing more liquid than is available in the wells. This is weird."
                )
        # do we actually have enough liquid in our wells to do this?

        ReturnWellSolutionTrackerInstance = WellSolutionTracker()

        for (
            WellSolutionInstance
        ) in SourceWellSolutionTrackerInstance.GetObjectsAsList():

            OriginalVolume = WellSolutionInstance.GetVolume()
            RemovedVolume = OriginalVolume * (OriginalVolume / WellVolume)
            NewVolume = OriginalVolume - RemovedVolume
            # This seems right but should be double checked TODO

            ReturnWellSolutionTrackerInstance.ManualLoad(
                WellSolution(WellSolutionInstance.GetReagent(), RemovedVolume)
            )
            # We have to return a unique WellSolution instance because it will be tracked in the destination

            WellSolutionInstance.Volume = NewVolume

            if NewVolume <= 0:
                SourceWellSolutionTrackerInstance.ManualUnload(WellSolutionInstance)

        return ReturnWellSolutionTrackerInstance

    def Dispense(
        self, WellNumber: int, WellSolutionTrackerInstance: WellSolutionTracker
    ):
        if not self.GetWellTracker().IsTracked(WellNumber):
            self.GetWellTracker().ManualLoad(Well(WellNumber))
        # If it doesn't exist then lets add it

        WellInstance = self.GetWellTracker().GetObjectByName(WellNumber)

        DestinationWellSolutionTrackerInstance = WellInstance.GetWellSolutionTracker()

        for WellSolutionInstance in WellSolutionTrackerInstance.GetObjectsAsList():
            if DestinationWellSolutionTrackerInstance.IsTracked(
                WellSolutionInstance.GetName()
            ):
                TrackedWellSolutionInstance = (
                    DestinationWellSolutionTrackerInstance.GetObjectByName(
                        WellSolutionInstance.GetName()
                    )
                )

                TrackedWellSolutionInstance.Volume += WellSolutionInstance.GetVolume()

            else:
                DestinationWellSolutionTrackerInstance.ManualLoad(WellSolutionInstance)
            # If the solution is already tracked then we remove it and add a new updated solution. Basically updating the volume of the solution

        WellVolume = sum(
            Solution.GetVolume()
            for Solution in DestinationWellSolutionTrackerInstance.GetObjectsAsList()
        )
        if WellVolume > WellInstance.MaxWellVolume:
            WellInstance.MaxWellVolume = WellVolume
        # We also check if the new volume is greater than the current max
