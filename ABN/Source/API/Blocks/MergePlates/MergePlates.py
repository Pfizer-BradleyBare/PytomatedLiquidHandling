from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal
from ...Blocks import SplitPlate
from ...Tools.Context import Context


@ClassDecorator_AvailableBlock
class MergePlates(Block):
    MergedPathwayInstances: list[SplitPlate] = list()
    WaitingMergeInstances: list[Block] = list()

    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Merge Plates" + str((self.Row, self.Col))

    def GetPlateName(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetMergeType(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        ProcessingMergeInstanceMergeType = self.GetMergeType()

        SplitPlateBlockInstance: SplitPlate = self
        while True:
            SearchBlockInstance = SplitPlateBlockInstance.GetParentNode()

            if SearchBlockInstance is None:
                break

            if (
                type(SplitPlateBlockInstance).__name__ == SplitPlate.__name__
                and SplitPlateBlockInstance not in MergePlates.MergedPathwayInstances
            ):
                break
        # Does this step come after a SplitPlate step? Lets Check

        # Do input validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()
        InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()
        # Get Context Trackers

        InactiveContextTrackerInstance.ManualLoad(
            WorkbookInstance.GetExecutingContext()
        )
        # First thing we need to do is disable this context. If both pathways are merged then we will re-enable the context

        MergePlates.WaitingMergeInstances.append(self)
        # Now we will add ourself to the waiting instances.

        WaitingMergeInstance: MergePlates = None
        for MergeInstance in MergePlates.WaitingMergeInstances:
            if MergeInstance.GetParentPlateName() == self.GetPlateName():
                WaitingMergeInstance = MergeInstance

        if WaitingMergeInstance is None:
            return
        # The other merge plates step hasn't been run yet. We need to wait for it to run. Return

        MergePlates.WaitingMergeInstances.remove(self)
        MergePlates.WaitingMergeInstances.remove(WaitingMergeInstance)
        # We are going to do the merge so these steps are no longer waiting

        WaitingMergeInstanceContext = ContextTrackerInstance.GetObjectByName(
            WaitingMergeInstance.Context()
        )
        ProcessingMergeInstanceContext = ContextTrackerInstance.GetObjectByName(
            self.Context()
        )
        # Get Merge Instance Contexts

        WaitingMergeInstanceMergeType = WaitingMergeInstance.GetMergeType()

        if (
            WaitingMergeInstanceMergeType == "Yes"
            and ProcessingMergeInstanceMergeType == "Yes"
        ):

            InactiveContextTrackerInstance.ManualUnload(ProcessingMergeInstanceContext)
            InactiveContextTrackerInstance.ManualUnload(WaitingMergeInstanceContext)
        # If both merge plate steps continue here then all we need to do is re-enable the pathways
        # This is not an official merge because pathways are not combined

        else:
            MergePlates.MergedPathwayInstances.append(SplitPlateBlockInstance)

            UpdateContextFactorsFlag = True
            if (
                SplitPlateBlockInstance.GetPathwayChoice() == "Split"
                or SplitPlateBlockInstance.GetPathwayChoice() == "Concurrent"
            ):
                UpdateContextFactorsFlag = False

            def CombineContexts(
                DestinationContextInstance: Context,
                SourceContextInstance: Context,
            ):
                for (
                    WellFactorInstance,
                    AspirateWellSequencesInstance,
                    DispenseWellSequencesInstance,
                ) in zip(
                    SourceContextInstance.GetWellFactorTracker().GetObjectsAsList(),
                    SourceContextInstance.GetAspirateWellSequencesTracker().GetObjectsAsList(),
                    SourceContextInstance.GetDispenseWellSequencesTracker().GetObjectsAsList(),
                ):
                    DestinationContextInstance.GetWellFactorTracker().ManualLoad(
                        WellFactorInstance
                    )
                    DestinationContextInstance.GetAspirateWellSequencesTracker().ManualLoad(
                        AspirateWellSequencesInstance
                    )
                    DestinationContextInstance.GetDispenseWellSequencesTracker().ManualLoad(
                        DispenseWellSequencesInstance
                    )

            # It is guarenteed that the wells in one pathway to do not overlap with the other merging pathway

            if WaitingMergeInstanceMergeType == "Yes":
                InactiveContextTrackerInstance.ManualUnload(WaitingMergeInstanceContext)

                if UpdateContextFactorsFlag is True:
                    CombineContexts(
                        WaitingMergeInstanceContext,
                        ProcessingMergeInstanceContext,
                    )

            elif ProcessingMergeInstanceMergeType == "Yes":
                InactiveContextTrackerInstance.ManualUnload(
                    ProcessingMergeInstanceContext
                )

                if UpdateContextFactorsFlag is True:
                    CombineContexts(
                        ProcessingMergeInstanceContext,
                        WaitingMergeInstanceContext,
                    )
