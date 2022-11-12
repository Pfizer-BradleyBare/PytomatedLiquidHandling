from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)
from ....Tools import Excel, ExcelOperator
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Context import WellSequence


@ClassDecorator_AvailableBlock
class Aliquot(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Aliquot" + str((self.Row, self.Col))

    def GetLocation(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 2, self.Col + 2)

    def GetStartPosition(self) -> str:
        with ExcelOperator(False, self.ExcelInstance) as ExcelOperatorInstance:
            ExcelOperatorInstance.SelectSheet("Method")
            return ExcelOperatorInstance.ReadCellValue(self.Row + 3, self.Col + 2)

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
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
