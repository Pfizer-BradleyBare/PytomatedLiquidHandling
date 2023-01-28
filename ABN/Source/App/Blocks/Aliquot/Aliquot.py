from typing import cast

from ...Tools import InputChecker
from ...Tools.Excel import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Aliquot(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetLocation(self, WorkbookInstance: Workbook) -> list[int]:

        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1),
            [int],
            [],
            [
                bool(Factor.GetFactor())
                for Factor in WorkbookInstance.GetContextTracker()
                .GetObjectByName(self.GetContext())
                .GetWellFactorTracker()
                .GetObjectsAsList()
            ],
        )

    def GetStartPosition(self, WorkbookInstance: Workbook) -> str:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1),
            [str],
            [],
            [
                bool(Factor.GetFactor())
                for Factor in WorkbookInstance.GetContextTracker()
                .GetObjectByName(self.GetContext())
                .GetWellFactorTracker()
                .GetObjectsAsList()
            ],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        Locations = self.GetLocation(WorkbookInstance)

        WorklistInstance = WorkbookInstance.GetWorklist()

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
