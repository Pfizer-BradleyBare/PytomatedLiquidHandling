from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class Vacuum(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.Source = BlockParameter.List[str](self, 1)
        self.Volume = BlockParameter.List[int | float](self, 2)
        self.VacuumPlate = BlockParameter.Item[str](self, 3)
        self.HoldTime = BlockParameter.Item[int | float](self, 4)
        self.PressureDifference = BlockParameter.Item[str | int | float](
            self, 5, ["Low", "Normal", "High"] + list(range(0, 1500))
        )
        self.VacuumTime = BlockParameter.Item[int | float](self, 6)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        ...
