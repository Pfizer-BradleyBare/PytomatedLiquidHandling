from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
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
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetStartPosition(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

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
