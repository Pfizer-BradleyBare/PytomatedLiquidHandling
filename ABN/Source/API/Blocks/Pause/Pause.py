from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook


@ClassDecorator_AvailableBlock
class Pause(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Pause" + str((self.Row, self.Col))

    def GetTime(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def Process(self, WorkbookInstance: Workbook):
        raise NotImplementedError
