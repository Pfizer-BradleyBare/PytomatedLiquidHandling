from ...Tools.Context import WellSequence
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

    def GetLocation(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1)

    def GetStartPosition(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        Locations = self.GetLocation()

        WorklistInstance = WorkbookInstance.GetWorklist()

        if WorklistInstance.IsWorklistColumn(Locations):
            Locations = WorklistInstance.ReadWorklistColumn(Locations)
        else:
            Locations = WorklistInstance.ConvertToWorklistColumn(int(Locations))

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
                DispenseSequencesTrackerInstance.ManualUnload(SequenceInstance)
                DispenseSequencesTrackerInstance.ManualLoad(
                    WellSequence(WellNumber, Location)
                )
        # We just need to update the Sequence in the ones that are different. Easy?

        return True
