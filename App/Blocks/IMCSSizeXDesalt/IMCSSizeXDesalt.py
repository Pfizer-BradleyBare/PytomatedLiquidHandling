from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class IMCSSizeXDesalt(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.Source = BlockParameter.Item[str](self, 1)
        self.Waste = BlockParameter.Item[str](self, 2)
        self.EQBuffer = BlockParameter.List[str](self, 3)
        self.LoadVolume = BlockParameter.Item[str | int | float](self, 4)
        self.ElutionMethod = BlockParameter.Item[str](self, 5)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:
        ...
