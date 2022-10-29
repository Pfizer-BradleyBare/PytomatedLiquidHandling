from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Context import WellSequences


@ClassDecorator_AvailableBlock
class Pool(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Pool" + str((self.Row, self.Col))

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
            WorkbookInstance.GetExecutingContext().GetDispenseWellSequencesTracker()
        )

        for SequenceInstance in DispenseSequencesTrackerInstance.GetObjectsAsList():
            DispenseSequencesTrackerInstance.ManualUnload(SequenceInstance)
        # We have to remve all the sequences before we start to reload

        for UniqueLocation in set(Locations):
            WellSequencesList: list[int] = list()
            for Location, WellNumber in zip(
                Locations,
                range(0, len(Locations)),
            ):
                if Location == UniqueLocation:
                    WellSequencesList.append(WellNumber)
            DispenseSequencesTrackerInstance.ManualLoad(
                WellSequences(UniqueLocation, WellSequencesList)
            )
        # We need to read the pool locations then adjust the dispense sequences
