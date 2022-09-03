from ....Tools import Excel


class Worklist:
    def __init__(self, ExcelInstance: Excel):
        self.ExcelInstance: Excel = ExcelInstance
        self.NumSamples: int = len(self.ReadWorklistColumn("Sample Number"))

    def GetNumSamples(self) -> int:
        return self.NumSamples

    def IsColumnDataValid(self, Data: list[any]) -> bool:
        return len(Data) == self.GetNumSamples()

    def IsWorklistColumn(self, ColumnName: str) -> bool:
        Data = self.ExcelInstance.ReadWorklistSheet()
        try:
            Data[0].index(ColumnName)
            return True
        except Exception:
            return False

    def ReadWorklistColumn(self, ColumnName: str) -> list[any]:
        Data = self.ExcelInstance.ReadWorklistSheet()

        Index = Data[0].index(ColumnName)

        OutputList = list()
        for Col in Data[1:]:
            if Col[Index] is None:
                break

            OutputList.append(Col[Index])

        return OutputList

    def WriteWorklistColumn(self, ColumnName: str, Data: list[any]):
        ReadData = self.ExcelInstance.ReadWorklistSheet()

        Index = ReadData[0].index(ColumnName) + 1

        self.ExcelInstance.WriteWorklistSheet(2, Index, [[Item] for Item in Data])
