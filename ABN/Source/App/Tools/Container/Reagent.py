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

    def GetLiquidClassCategory(self) -> LiquidClassCategory:
        with ExcelHandle(False) as ExcelHandleInstance:
            self.ExcelInstance.AttachHandle(ExcelHandleInstance)

            self.ExcelInstance.SelectSheet("Solutions")

        return LiquidClassCategory(
            self.ExcelInstance.ReadCellValue(4, 2),
            self.ExcelInstance.ReadCellValue(5, 2),
            self.ExcelInstance.ReadCellValue(6, 2),
            self.ExcelInstance.ReadCellValue(7, 2),
        )
