from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal


@ClassDecorator_AvailableBlock
class Vacuum(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Vacuum" + str((self.Row, self.Col))

    def GetSource(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetVolume(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def GetVacuumPlate(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 4, self.Col + 2, self.Row + 4, self.Col + 2
        )

    def GetPreVacuumWaitTime(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 5, self.Col + 2, self.Row + 5, self.Col + 2
        )

    def GetPressureDifference(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 6, self.Col + 2, self.Row + 6, self.Col + 2
        )

    def GetVacuumTime(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 7, self.Col + 2, self.Row + 7, self.Col + 2
        )

    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass
