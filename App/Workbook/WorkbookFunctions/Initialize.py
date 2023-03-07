from PytomatedLiquidHandling.API.Tools.Container import ContainerTracker
from PytomatedLiquidHandling.API.Tools.RunTypes.RunTypes import RunTypes

from ...Tools.Container import Plate
from ...Tools.Context import (
    Context,
    ContextTracker,
    WellFactor,
    WellFactorTracker,
    WellSequence,
    WellSequenceTracker,
)
from ...Workbook import BlockTracker, Workbook
from ..Solution import SolutionLoader


def Initialize(WorkbookInstance: Workbook):
    WorkbookInstance.ExcelInstance.OpenBook(False)
    # Setup special varibles

    # Trackers
    WorkbookInstance.ExecutedBlocksTrackerInstance = BlockTracker()
    WorkbookInstance.ContainerTrackerInstance = ContainerTracker()
    WorkbookInstance.ContextTrackerInstance = ContextTracker()
    WorkbookInstance.ContextTrackerInstance = ContextTracker()
    WorkbookInstance.InactiveContextTrackerInstance = ContextTracker()
    WorkbookInstance.CompletedPreprocessingBlocksTrackerInstance = BlockTracker()

    # Set Initial Active Context
    AspirateWellSequenceTrackerInstance = WellSequenceTracker()
    DispenseWellSequenceTrackerInstance = WellSequenceTracker()

    WellFactorsTrackerInstance = WellFactorTracker()

    for SampleNumber in range(1, WorkbookInstance.GetWorklist().GetNumSamples() + 1):
        WellNumber = SampleNumber

        WellSequencesInstance = WellSequence(WellNumber, WellNumber)
        WellFactorInstance = WellFactor(WellNumber, 1)

        AspirateWellSequenceTrackerInstance.ManualLoad(WellSequencesInstance)
        DispenseWellSequenceTrackerInstance.ManualLoad(WellSequencesInstance)

        WellFactorsTrackerInstance.ManualLoad(WellFactorInstance)

    WorkbookInstance.SetExecutingContext(
        Context(
            ":__StartingContext__",
            AspirateWellSequenceTrackerInstance,
            DispenseWellSequenceTrackerInstance,
            WellFactorsTrackerInstance,
        )
    )

    WorkbookInstance.GetContextTracker().ManualLoad(
        WorkbookInstance.GetExecutingContext()
    )

    WorkbookInstance.GetContainerTracker().PlateTrackerInstance.ManualLoad(
        Plate(
            "__StartingContext__", WorkbookInstance.GetName(), "No Preference"
        )  # This will never be loaded so filter doesn't matter
    )

    WorkbookInstance.GetContainerTracker().ReagentTrackerInstance = SolutionLoader.Load(
        WorkbookInstance.GetName(),
        WorkbookInstance.ExcelInstance,
        WorkbookInstance.GetWorklist(),
    )
    # We do need to do some checks to ensure consistency.
    # TODO: Are all reagents in the labware selection... Etc.

    # Setting initial context and container.
    if WorkbookInstance.GetRunType() == RunTypes.Run:
        pass
        # WorkbookInstance.ProcessingLock.acquire()

    # TODO WorkbookInstance.RunType = WorkbookInstance.GetRunType() != RunTypes.Run

    WorkbookInstance.ExcelInstance.CloseBook()
