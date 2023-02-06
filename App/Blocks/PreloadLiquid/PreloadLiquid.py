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

        # Params
        self.Source = BlockParameter.Item[str](self, 1, [self.GetParentPlateName()])
        self.Volume = BlockParameter.List[int | float](self, 2)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        ParentContainer = (
            WorkbookInstance.GetContainerTracker()
            .GetPlateTracker()
            .GetObjectByName(self.Source.Read(WorkbookInstance))
        )

        WellFactorTrackerInstance = (
            WorkbookInstance.GetExecutingContext().GetWellFactorTracker()
        )

        Volumes = self.Volume.Read(WorkbookInstance)

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
