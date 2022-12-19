from ....Tools.AbstractClasses import ObjectABC
from ...Workbook.Solution import SolutionPropertyValues, SolutionTracker
from ...Workbook.Solution.Value.Value import SolutionPropertyValue
from .Container import Container
from .Well.Solution.WellSolution import WellSolution
from .Well.Solution.WellSolutionTracker import WellSolutionTracker
from .Well.Well import Well


class ContainerOperator:
    def __init__(self, ContainerInstance: Container):
        self.ContainerInstance: Container = ContainerInstance

    def Aspirate(
        self,
        WellNumber: int,
        Volume: float,
    ) -> WellSolutionTracker:

        if not self.ContainerInstance.GetWellTracker().IsTracked(WellNumber):
            self.ContainerInstance.GetWellTracker().ManualLoad(Well(WellNumber))
        # If it doesn't exist then lets add it

        WellInstance = self.ContainerInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        SourceWellSolutionTrackerInstance = WellInstance.GetWellSolutionTracker()

        WellVolume = sum(
            Solution.GetVolume()
            for Solution in SourceWellSolutionTrackerInstance.GetObjectsAsList()
        )

        if WellVolume != 0:
            if Volume > WellVolume:
                raise Exception(
                    "You are removing more liquid than is available in the wells. This is weird."
                )

        ReturnWellSolutionTrackerInstance = WellSolutionTracker()

        if WellVolume == 0:
            ReturnWellSolutionTrackerInstance.ManualLoad(
                WellSolution(self.ContainerInstance.GetName(), Volume)
            )
            # We have to return a unique WellSolution instance because it will be tracked in the destination
            WellInstance.MinWellVolume -= Volume

        # We are pipetting from a reagent source

        else:
            for (
                WellSolutionInstance
            ) in SourceWellSolutionTrackerInstance.GetObjectsAsList():

                OriginalVolume = WellSolutionInstance.GetVolume()
                RemovedVolume = OriginalVolume * (OriginalVolume / WellVolume)
                NewVolume = OriginalVolume - RemovedVolume
                # This seems right but should be double checked TODO

                ReturnWellSolutionTrackerInstance.ManualLoad(
                    WellSolution(WellSolutionInstance.GetName(), RemovedVolume)
                )
                # We have to return a unique WellSolution instance because it will be tracked in the destination

                WellSolutionInstance.Volume = NewVolume

                if NewVolume <= 0:
                    SourceWellSolutionTrackerInstance.ManualUnload(WellSolutionInstance)
            # We are pipetting from a plate source

        return ReturnWellSolutionTrackerInstance

    def Dispense(
        self,
        WellNumber: int,
        SourceWellSolutionTrackerInstance: WellSolutionTracker,
    ):

        if not self.ContainerInstance.GetWellTracker().IsTracked(WellNumber):
            self.ContainerInstance.GetWellTracker().ManualLoad(Well(WellNumber))
        # If it doesn't exist then lets add it

        WellInstance = self.ContainerInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        DestinationWellSolutionTrackerInstance = WellInstance.GetWellSolutionTracker()

        for (
            WellSolutionInstance
        ) in SourceWellSolutionTrackerInstance.GetObjectsAsList():
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

    # This is defined inside the ContainerOperator class because it is only used within this class. We do NOT want to expose this anywhere else.
    # On the other hand a liquid class is well specific so maybe it should be there... I digress
    class LiquidClass(ObjectABC):
        def __init__(
            self,
            Volatility: SolutionPropertyValue,
            Viscosity: SolutionPropertyValue,
            Homogeneity: SolutionPropertyValue,
            LLD: SolutionPropertyValue,
        ):
            self.Volatility: SolutionPropertyValue = Volatility
            self.Viscosity: SolutionPropertyValue = Viscosity
            self.Homogeneity: SolutionPropertyValue = Homogeneity
            self.LLD: SolutionPropertyValue = LLD

        def GetName(self) -> str:
            return (
                self.Volatility.GetName()
                + self.Viscosity.GetName()
                + self.Homogeneity.GetName()
                + self.LLD.GetName()
            ).replace(" ", "")

        def GetVolatility(self) -> SolutionPropertyValue:
            return self.Volatility

        def GetViscosity(self) -> SolutionPropertyValue:
            return self.Viscosity

        def GetHomogeneity(self) -> SolutionPropertyValue:
            return self.Homogeneity

        def GetLLD(self) -> SolutionPropertyValue:
            return self.LLD

        def GetMinAspirateMixParam(self):
            ReturnMinMixParam = 0

            MinMixParam = self.GetVolatility().GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetViscosity().GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetHomogeneity().GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetLLD().GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            return ReturnMinMixParam

        def GetMinDispenseMixParam(self):
            ReturnMinMixParam = 0

            MinMixParam = self.GetVolatility().GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetViscosity().GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetHomogeneity().GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetLLD().GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            return ReturnMinMixParam

    # Liquid class is the combo of Volatility, Viscosity, Homogeneity, and LLD
    def GetLiquidClass(
        self,
        SolutionTrackerInstance: SolutionTracker,
        WellNumber: int,
    ) -> LiquidClass:
        WellInstance = self.ContainerInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        WellSolutionInstances = WellInstance.GetWellSolutionTracker().GetObjectsAsList()

        WellVolume = sum(Solution.GetVolume() for Solution in WellSolutionInstances)
        # A solution will technically not have a well volume because we never pipette into a solution. Only out of

        if WellVolume == 0:
            ContainerName = self.ContainerInstance.GetName()
            Volatility = SolutionTrackerInstance.GetObjectByName(
                ContainerName
            ).GetVolatility()
            Viscosity = SolutionTrackerInstance.GetObjectByName(
                ContainerName
            ).GetViscosity()
            Homogeneity = SolutionTrackerInstance.GetObjectByName(
                ContainerName
            ).GetHomogeneity()
            LLD = SolutionTrackerInstance.GetObjectByName(ContainerName).GetLLD()

        else:
            VolatilityList = list()
            ViscosityList = list()
            HomogeneityList = list()
            LLDList = list()

            for WellSolutionInstance in WellSolutionInstances:
                Percentage = int(WellSolutionInstance.GetVolume() * 100 / WellVolume)

                SolutionInstance = SolutionTrackerInstance.GetObjectByName(
                    WellSolutionInstance.GetName()
                )

                VolatilityList += (
                    [SolutionInstance.GetVolatility().GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetVolatility().GetWeight()
                )

                ViscosityList += (
                    [SolutionInstance.GetViscosity().GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetViscosity().GetWeight()
                )

                HomogeneityList += (
                    [SolutionInstance.GetHomogeneity().GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetHomogeneity().GetWeight()
                )

                LLDList += (
                    [SolutionInstance.GetLLD().GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetLLD().GetWeight()
                )

            Volatility = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(VolatilityList) / len(VolatilityList)))
            )

            Viscosity = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(ViscosityList) / len(ViscosityList)))
            )

            Homogeneity = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(HomogeneityList) / len(HomogeneityList)))
            )

            LLD = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(LLDList) / len(LLDList)))
            )
            # We are going to process the whole shebang here

        return ContainerOperator.LiquidClass(Volatility, Viscosity, Homogeneity, LLD)
