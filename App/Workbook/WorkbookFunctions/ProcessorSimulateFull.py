import threading

from PytomatedLiquidHandling.API.Tools.LabwareSelection import LabwareSelectionLoader

from ...Blocks import MergePlates
from ...Workbook import Block, Workbook, WorkbookFunctions


def ProcessorSimulateFull(WorkbookInstance: Workbook):

    # We need to create some "Imaginary" plates to do the partial simulation.

    # We need to do the run. The run processor is what we want to simulate so we will just call that method
    WorkbookFunctions.ProcessorRun(WorkbookInstance)

    # Now we need to wait for the user to load plates before doing the full run.
