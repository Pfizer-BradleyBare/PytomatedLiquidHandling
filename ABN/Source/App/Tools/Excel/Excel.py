import threading

import pythoncom
import xlwings

from ....Globals import GetLogger

Lock = threading.Lock()


def ExcelClassFunctionDecorator_ThreadLock(DecoratedFunction):
    def inner(*args, **kwargs):
        LoggerInstance = GetLogger()

        LoggerInstance.debug("Start Excel Function: " + DecoratedFunction.__name__)
        LoggerInstance.debug("Args: " + str(args))

        if args[0].Book is not None:
            Lock.acquire()
            Result = DecoratedFunction(*args, **kwargs)
            Lock.release()
        else:
            LoggerInstance.critical("Excel book is not open! No action performed")
            Result = None

        LoggerInstance.debug("End Excel Function: " + DecoratedFunction.__name__)
        return Result

    return inner


class Excel:
    def __init__(self, ExcelFilePath: str):
        self.ExcelFilePath: str = ExcelFilePath

        self.Book: xlwings.Book | None = None
        self.App: xlwings.App | None = None

    def __AlignArray(self, Array: list[list[any]]):  # type:ignore
        Max = max(len(i) for i in Array)
        for List in Array:
            List += [None] * (Max - len(List))

    def __AlignTuple(self, Array: tuple[tuple[any]]):  # type:ignore
        Max = max(len(i) for i in Array)
        for Tuple in Array:
            Tuple += (None,) * (Max - len(Tuple))

    def GetExcelFilePath(self) -> str:
        return self.ExcelFilePath

    def GetBook(self) -> xlwings.Book:
        if self.Book is None:
            raise Exception("Book not open. Please correct...")

        return self.Book

    def OpenBook(self, Visible: bool):
        if self.Book is not None:
            return

        if xlwings.apps.count != 0:
            for Book in xlwings.books:
                if Book.fullname == self.ExcelFilePath:
                    self.App = Book.app
                    self.Book = Book

        if self.App is not None:
            if self.App.visible != Visible:
                self.CloseBook()

        if self.App is None:
            pythoncom.CoInitialize()  # Required for some reason.
            self.App = xlwings.App(visible=Visible, add_book=False)
            self.Book = self.App.books.open(self.ExcelFilePath)

    def CloseBook(self):
        Book = self.GetBook()
        # Check book is open

        Book.save()
        Book.close()

        if self.App is not None:
            if len(self.App.books) == 0:
                self.App.quit()

        self.Book = None
        self.App = None

    @ExcelClassFunctionDecorator_ThreadLock
    def Save(self):
        self.GetBook().save()

    @ExcelClassFunctionDecorator_ThreadLock
    def CreateSheet(self, Name: str):
        self.GetBook().sheets.add(name=Name, after="Solutions")

    @ExcelClassFunctionDecorator_ThreadLock
    def DeleteSheet(self, Name: str):
        self.GetBook().sheets[Name].delete()

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadCellValue(self, SheetName: str, Row: int, Col: int) -> object:
        return self.GetBook().sheets[SheetName].range((Row, Col), (Row, Col)).value

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadCellFormula(self, SheetName: str, Row: int, Col: int) -> object:
        return self.GetBook().sheets[SheetName].range((Row, Col), (Row, Col)).formula

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadRangeValues(
        self,
        SheetName: str,
        RowStart: int,
        ColStart: int,
        RowEnd: int,
        ColEnd: int,
    ) -> list[list[object]]:
        return (
            self.GetBook()
            .sheets[SheetName]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
            .options(ndim=2)
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadRangeFormulas(
        self,
        SheetName: str,
        RowStart: int,
        ColStart: int,
        RowEnd: int,
        ColEnd: int,
    ) -> tuple[tuple[object]]:
        return (
            self.GetBook()
            .sheets[SheetName]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
            .options(ndim=2)
            .formula
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteCellValue(self, SheetName: str, Row: int, Col: int, Data: object):
        self.GetBook().sheets[SheetName].range((Row, Col), (Row, Col)).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteCellFormula(self, SheetName: str, Row: int, Col: int, Data: object):
        self.GetBook().sheets[SheetName].range((Row, Col), (Row, Col)).formula = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteRangeValues(
        self,
        SheetName: str,
        RowStart: int,
        ColStart: int,
        Data: list[list[object]],
    ):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])

        self.GetBook().sheets[SheetName].range(
            (RowStart, ColStart), (RowStart + NumRows - 1, ColStart + NumCols - 1)
        ).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteRangeFormulas(
        self,
        SheetName: str,
        RowStart: int,
        ColStart: int,
        Data: tuple[tuple[object]],
    ):
        self.__AlignTuple(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])

        self.GetBook().sheets[SheetName].range(
            (RowStart, ColStart), (RowStart + NumRows - 1, ColStart + NumCols - 1)
        ).formula = Data
