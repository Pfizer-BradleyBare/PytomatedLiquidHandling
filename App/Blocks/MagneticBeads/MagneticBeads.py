from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class MagneticBeads(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.BeadsPlate = BlockParameter.Item[str](self, 1)
        self.StorageBuffer = BlockParameter.List[str](self, 2)
        self.BufferVolume = BlockParameter.List[int | float](self, 3)
        self.HoldTime = BlockParameter.List[int | float](self, 4)
        self.Repetitions = BlockParameter.List[int | float](self, 5)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        ...
