import xlwings as xl
import threading
from ...Server.Globals import LOG

ExcelLock = threading.Lock()


def ExcelClassFunctionDecorator_ThreadLock(DecoratedFunction):
    def inner(*args, **kwargs):
        ExcelLock.acquire()
        LOG.debug("ExcelLock Acquired: " + DecoratedFunction.__name__)

        Result = DecoratedFunction(*args, **kwargs)

        ExcelLock.release()
        LOG.debug("ExcelLock Released: " + DecoratedFunction.__name__)
        return Result

    return inner


class Excel:
    def __init__(self, ExcelFilePath: str):
        self.ExcelFilePath: str = ExcelFilePath

    def __AlignArray(self, Array: list[list[any]]):  # type:ignore
        Max = max(len(i) for i in Array)
        for List in Array:
            List += [None] * (Max - len(List))

    @ExcelClassFunctionDecorator_ThreadLock
    def CreateSheet(self, Name: str):
        xl.Book(self.ExcelFilePath).sheets.add(name=Name, after="Solutions")

    @ExcelClassFunctionDecorator_ThreadLock
    def DeleteSheet(self, Name: str):
        xl.Book(self.ExcelFilePath).sheets[Name].delete()

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadMethodSheet(self) -> list[list[any]]:  # type:ignore
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Method"]
            .range((1, 1), (1500, 100))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadMethodSheetArea(
        self, RowStart: int, ColStart: int, RowEnd: int, ColEnd: int
    ):
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Method"]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteMethodSheet(self, Row: int, Col: int, Data: list[list[str]]):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])
        xl.Book(self.ExcelFilePath).sheets["Method"].range(
            (Row, Col), (Row + NumRows, Col + NumCols)
        ).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadWorklistSheet(self) -> list[list[any]]:  # type:ignore
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Worklist"]
            .range((1, 1), (500, 100))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadWorklistSheetArea(
        self, RowStart: int, ColStart: int, RowEnd: int, ColEnd: int
    ):
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Worklist"]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteWorklistSheet(self, Row: int, Col: int, Data: list[list[str]]):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])
        xl.Book(self.ExcelFilePath).sheets["Worklist"].range(
            (Row, Col), (Row + NumRows, Col + NumCols)
        ).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadSolutionsSheet(self) -> list[list[any]]:  # type:ignore
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Solutions"]
            .range((1, 1), (200, 50))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadSolutionsSheetArea(
        self, RowStart: int, ColStart: int, RowEnd: int, ColEnd: int
    ):
        return (
            xl.Book(self.ExcelFilePath)
            .sheets["Solutions"]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteSolutionsSheet(self, Row: int, Col: int, Data: list[list[str]]):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])
        xl.Book(self.ExcelFilePath).sheets["Solutions"].range(
            (Row, Col), (Row + NumRows, Col + NumCols)
        ).value = Data
