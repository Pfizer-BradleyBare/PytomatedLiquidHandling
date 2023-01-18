from ....API.Tools.Container import Reagent as APIReagent
from ....API.Tools.Container.BaseContainer import LiquidClassCategory
from ..Excel import Excel, ExcelHandle


class Reagent(APIReagent):
    def __init__(
        self,
        Name: str,
        MethodName: str,
        PreferredLabware: str,
        ExcelInstance: Excel,
        Row: int,
        Col: int,
    ):
        APIReagent.__init__(
            self, Name, MethodName, None, None, None, None  # type:ignore
        )
        self.Filter.append(PreferredLabware)

        self.PreferredLabware: str = PreferredLabware
        self.ExcelInstance: Excel = ExcelInstance
        self.Row: int = Row
        self.Col: int = Col

    def IsCorrectSolution(self) -> bool:
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

            self.ExcelInstance.SelectSheet("Solutions")

            return self.ExcelInstance.ReadCellValue(self.Row, self.Col) == self.Name

    def GetLiquidClassCategory(self) -> LiquidClassCategory:
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

            self.ExcelInstance.SelectSheet("Solutions")

            return LiquidClassCategory(
                self.ExcelInstance.ReadCellValue(self.Row + 3, self.Col + 1),
                self.ExcelInstance.ReadCellValue(self.Row + 4, self.Col + 1),
                self.ExcelInstance.ReadCellValue(self.Row + 5, self.Col + 1),
                self.ExcelInstance.ReadCellValue(self.Row + 6, self.Col + 1),
            )
