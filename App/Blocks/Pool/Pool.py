from ...Tools import BlockParameter
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

        # Params
        self.Location = BlockParameter.List[int](self, 1)
        self.StartPosition = BlockParameter.Item[str](
            self,
            2,
            ["Sample Start Position", "Plate Start Position(A1)"],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        Locations = self.Location.Read(WorkbookInstance)

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
