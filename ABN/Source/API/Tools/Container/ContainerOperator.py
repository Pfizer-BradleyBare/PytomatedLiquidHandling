from ...Workbook.Block import Block
from .Container import Container
from .Well.Solution.WellSolutionTracker import WellSolutionTracker
from .Well.Solution.WellSolution import WellSolution


class ContainerOperator:
    def __init__(self, ContainerInstance: Container, BlockInstance: Block):
        self.ContainerInstance: Container = ContainerInstance
        self.BlockInstance: Block = BlockInstance

    def Dispense(
        self, WellNumber: int, SourceWellSolutionTrackerInstance: WellSolutionTracker
    ):
        if not self.ContainerInstance.GetDispenseBlockTracker().IsTracked(
            self.BlockInstance
        ):
            self.ContainerInstance.GetDispenseBlockTracker().ManualLoad(
                self.BlockInstance
            )

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

    def Aspirate(self, WellNumber: int, Volume: float) -> WellSolutionTracker:
        if not self.ContainerInstance.GetAspirateBlockTracker().IsTracked(
            self.BlockInstance
        ):
            self.ContainerInstance.GetAspirateBlockTracker().ManualLoad(
                self.BlockInstance
            )

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
