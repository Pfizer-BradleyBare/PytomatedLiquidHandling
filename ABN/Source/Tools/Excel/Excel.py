import xlwings as xl


class Excel:
    def __init__(self, ExcelFilePath: str):
        self.ExcelFilePath: str = ExcelFilePath

    def __AlignArray(self, Array: list[list[any]]):
        Max = max(len(i) for i in Array)
        for List in Array:
            List += [None] * (Max - len(List))

    def CreateSheet(self, Name: str):
        xl.Book(self.ExcelFilePath).sheets.add(name=Name, after="Solutions")

    def DeleteSheet(self, Name: str):
        xl.Book(self.ExcelFilePath).sheets[Name].delete()

    def ReadMethodSheet(self) -> list[list[any]]:
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Method"]
            .range((1, 1), (1500, 100))
            .value
        )

    def WriteMethodSheet(self, Row: int, Col: int, Data: list[list[str]]):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])
        xl.Book(self.ExcelFilePath).sheets["Method"].range(
            (Row, Col), (Row + NumRows, Col + NumCols)
        ).value = Data

    def ReadWorklistSheet(self) -> list[list[any]]:
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Worklist"]
            .range((1, 1), (500, 100))
            .value
        )

    def WriteWorklistSheet(self, Row: int, Col: int, Data: list[list[str]]):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])
        xl.Book(self.ExcelFilePath).sheets["Worklist"].range(
            (Row, Col), (Row + NumRows, Col + NumCols)
        ).value = Data

    def ReadWorklistColumn(self, ColumnName: str) -> list[any]:
        Data = self.ReadWorklistSheet()

        Index = Data[0].index(ColumnName)

        OutputList = list()
        for Col in Data[1:]:
            if Col[Index] is None:
                break

            OutputList.append(Col[Index])

        return OutputList

    def ReadSolutionsSheet(self) -> list[list[any]]:
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Solutions"]
            .range((1, 1), (200, 50))
            .value
        )

    def WriteSolutionsSheet(self, Row: int, Col: int, Data: list[list[str]]):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])
        xl.Book(self.ExcelFilePath).sheets["Solutions"].range(
            (Row, Col), (Row + NumRows, Col + NumCols)
        ).value = Data
