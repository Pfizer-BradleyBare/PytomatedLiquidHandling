from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class PreloadLiquid(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetSource(self, WorkbookInstance: Workbook) -> str:
        return InputChecker.CheckAndConvertItem(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1),
            [str],
            [self.GetParentPlateName()],
        )

    def GetVolume(self, WorkbookInstance: Workbook) -> list[int | float]:
        return InputChecker.CheckAndConvertList(
            WorkbookInstance,
            self,
            self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1),
            [int, float],
            [],
        )

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        ParentContainer = (
            WorkbookInstance.GetContainerTracker()
            .GetPlateTracker()
            .GetObjectByName(self.GetParentPlateName())
        )

        WellFactorTrackerInstance = (
            WorkbookInstance.GetExecutingContext().GetWellFactorTracker()
        )

        Volumes = self.GetVolume(WorkbookInstance)

        for WellNumber, Volume in zip(
            range(1, WorkbookInstance.WorklistInstance.GetNumSamples() + 1), Volumes
        ):
            if WellFactorTrackerInstance.GetObjectByName(WellNumber).GetFactor() == 0:
                continue

            AspirateSolutionTracker = ParentContainer.Aspirate(WellNumber, Volume)
            ParentContainer.Dispense(WellNumber, AspirateSolutionTracker)
            ParentContainer.Dispense(WellNumber, AspirateSolutionTracker)
            # This effectively removes a volume, returns to zero, then adds that additional volume because the plate should contain it.

        return True
