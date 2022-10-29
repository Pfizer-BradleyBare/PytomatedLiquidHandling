from ....Tools import Excel


class Worklist:
    def __init__(self, ExcelInstance: Excel):
        self.ExcelInstance: Excel = ExcelInstance

        # Determine number of samples
        Data = self.ExcelInstance.ReadWorklistSheet()

        ColIndex = Data[0].index("Sample Number")

        OutputList = list()
        for Col in Data[1:]:
            if Col[ColIndex] is None:
                break

            OutputList.append(Col[ColIndex])

        self.NumSamples = len(OutputList)

    def GetNumSamples(self) -> int:
        return self.NumSamples

    def IsColumnDataValid(self, Data: list[any]) -> bool:  # type:ignore
        return len(Data) == self.GetNumSamples()

    def IsWorklistColumn(self, ColumnName: str) -> bool:
        Data = self.ExcelInstance.ReadWorklistSheet()
        try:
            Data[0].index(ColumnName)
            return True
        except Exception:
            return False

    def ReadWorklistColumn(self, ColumnName: str) -> list[any]:  # type:ignore
        Data = self.ExcelInstance.ReadWorklistSheet()

        ColIndex = Data[0].index(ColumnName)

        return [
            Data[RowIndex][ColIndex] for RowIndex in range(1, 1 + self.GetNumSamples())
        ]

    def ConvertToWorklistColumn(self, Value: any) -> list[any]:  # type:ignore
        return [Value] * self.GetNumSamples()

    def WriteWorklistColumn(self, ColumnName: str, Data: list[any]):  # type:ignore
        ReadData = self.ExcelInstance.ReadWorklistSheet()

        Index = ReadData[0].index(ColumnName) + 1

        self.ExcelInstance.WriteWorklistSheet(2, Index, [[Item] for Item in Data])
