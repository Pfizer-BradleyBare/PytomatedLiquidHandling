from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook


@ClassDecorator_AvailableBlock
class MagneticBeads(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Magnetic Beads" + str((self.Row, self.Col))

    def GetMagneticBeadsPlate(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetStorageBuffer(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetStorageBufferVolume(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def GetHoldTime(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 5, self.Col + 2, self.Row + 5, self.Col + 2
        )

    def GetRepitions(self) -> str:
        self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 6, self.Col + 2, self.Row + 6, self.Col + 2
        )

    def Process(self, WorkbookInstance: Workbook):
        raise NotImplementedError
