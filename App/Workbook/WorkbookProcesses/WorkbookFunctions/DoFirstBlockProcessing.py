from ....Workbook import Block, Workbook


def DoFirstBlockProcessing(WorkbookInstance: Workbook):

    CurrentExecutingBlock: Block = WorkbookInstance.MethodTreeRoot
    CurrentExecutingBlock.Process(WorkbookInstance)
    WorkbookInstance.ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
