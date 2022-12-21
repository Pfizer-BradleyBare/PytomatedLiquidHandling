from ...Tools.Context import WellSequence
from ...Tools.Excel import Excel, ExcelHandle
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class Aliquot(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Aliquot" + str((self.Row, self.Col))

    def GetLocation(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetStartPosition(self) -> str:
        self.ExcelInstance.SelectSheet("Method")
        return self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook):
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

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
                if SequenceInstance.GetSequence() != Location:
                    DispenseSequencesTrackerInstance.ManualUnload(SequenceInstance)
                    DispenseSequencesTrackerInstance.ManualLoad(
                        WellSequence(WellNumber, Location)
                    )
            # We just need to update the Sequence in the ones that are different. Easy?
