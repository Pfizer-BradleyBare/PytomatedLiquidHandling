from ...Workbook.Block import Block
from ...Workbook.Solution import SolutionTracker, SolutionPropertyValues
from .Container import Container
from .Well.Solution.WellSolutionTracker import WellSolutionTracker
from .Well.Solution.WellSolution import WellSolution
from .Well.Well import Well


class ContainerOperator:
    def __init__(self, ContainerInstance: Container, BlockInstance: Block):
        self.ContainerInstance: Container = ContainerInstance
        self.BlockInstance: Block = BlockInstance

    def Aspirate(
        self,
        WellNumber: int,
        Volume: float,
    ) -> WellSolutionTracker:
        if not self.ContainerInstance.GetAspirateBlockTracker().IsTracked(
            self.BlockInstance
        ):
            self.ContainerInstance.GetAspirateBlockTracker().ManualLoad(
                self.BlockInstance
            )

        WellInstance = Well(WellNumber)
        if not self.ContainerInstance.GetWellTracker().IsTracked(WellInstance):
            self.ContainerInstance.GetWellTracker().ManualLoad(WellInstance)
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
            WellInstance.MinWellVolume -= Volume

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

                SourceWellSolutionTrackerInstance.ManualUnload(WellSolutionInstance)

                if NewVolume > 0:
                    SourceWellSolutionTrackerInstance.ManualLoad(
                        WellSolution(
                            WellSolutionInstance.GetName(),
                            NewVolume,
                        )
                    )

        return ReturnWellSolutionTrackerInstance

    def Dispense(
        self,
        WellNumber: int,
        SourceWellSolutionTrackerInstance: WellSolutionTracker,
    ):
        if not self.ContainerInstance.GetDispenseBlockTracker().IsTracked(
            self.BlockInstance
        ):
            self.ContainerInstance.GetDispenseBlockTracker().ManualLoad(
                self.BlockInstance
            )

        WellInstance = Well(WellNumber)
        if not self.ContainerInstance.GetWellTracker().IsTracked(WellInstance):
            self.ContainerInstance.GetWellTracker().ManualLoad(WellInstance)
        # If it doesn't exist then lets add it

        WellInstance = self.ContainerInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        DestinationWellSolutionTrackerInstance = WellInstance.GetWellSolutionTracker()

        for (
            WellSolutionInstance
        ) in SourceWellSolutionTrackerInstance.GetObjectsAsList():
            if DestinationWellSolutionTrackerInstance.IsTracked(WellSolutionInstance):
                TrackedWellSolution = (
                    DestinationWellSolutionTrackerInstance.GetObjectByName(
                        WellSolutionInstance.GetName()
                    )
                )
                DestinationWellSolutionTrackerInstance.ManualUnload(
                    WellSolutionInstance
                )

                UpdatedWellSolution = WellSolution(
                    WellSolutionInstance.GetName(),
                    WellSolutionInstance.GetVolume() + TrackedWellSolution.GetVolume(),
                )
                DestinationWellSolutionTrackerInstance.ManualLoad(UpdatedWellSolution)
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

    # Liquid class is the combo of Volatility, Viscosity, Homogeneity, and LLD
    def GetLiquidClass(
        self,
        SolutionTrackerInstance: SolutionTracker,
        WellNumber: int,
    ) -> str:
        WellInstance = self.ContainerInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        WellSolutionInstances = WellInstance.GetWellSolutionTracker().GetObjectsAsList()
        WellVolume = sum(Solution.GetVolume() for Solution in WellSolutionInstances)

        if WellVolume == 0:
            ContainerName = self.ContainerInstance.GetName()
            Volatility = (
                SolutionTrackerInstance.GetObjectByName(ContainerName)
                .GetVolatility()
                .GetName()
            )
            Viscosity = (
                SolutionTrackerInstance.GetObjectByName(ContainerName)
                .GetViscosity()
                .GetName()
            )
            Homogeneity = (
                SolutionTrackerInstance.GetObjectByName(ContainerName)
                .GetHomogeneity()
                .GetName()
            )
            LLD = (
                SolutionTrackerInstance.GetObjectByName(ContainerName)
                .GetLLD()
                .GetName()
            )

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
            ).GetName()

            Viscosity = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(ViscosityList) / len(ViscosityList)))
            ).GetName()

            Homogeneity = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(HomogeneityList) / len(HomogeneityList)))
            ).GetName()

            LLD = SolutionPropertyValues.GetObjectByNumericValue(
                int(round(sum(LLDList) / len(LLDList)))
            ).GetName()
            # We are going to process the whole shebang here

        return Volatility + Viscosity + Homogeneity + LLD
