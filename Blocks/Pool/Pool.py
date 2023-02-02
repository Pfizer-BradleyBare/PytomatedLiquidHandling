from ...Tools import InputChecker
from ...Tools.Context import WellSequence
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Pool(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetLocation(self, WorkbookInstance: Workbook) -> list[int]:

        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1),
            [int],
            [],
        )

    def GetStartPosition(self, WorkbookInstance: Workbook) -> str:

        return InputChecker.CheckAndConvertItem(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1),
            [str],
            ["Sample Start Position", "Plate Start Position(A1)"],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        Locations = self.GetLocation(WorkbookInstance)

        WorklistInstance = WorkbookInstance.GetWorklist()

        # do input validation here

        DispenseSequencesTrackerInstance = (
            WorkbookInstance.GetExecutingContext().GetDispenseWellSequenceTracker()
        )

        for WellNumber, Location in zip(
            range(0, WorklistInstance.GetNumSamples()), Locations
        ):
            SequenceInstance = DispenseSequencesTrackerInstance.GetObjectByName(
                WellNumber
            )
            if SequenceInstance.SequencePosition != Location:
                SequenceInstance.SequencePosition = Location
        # We just need to update the Sequence in the ones that are different. Easy?

        return True
