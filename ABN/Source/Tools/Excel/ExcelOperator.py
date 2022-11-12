from .Excel import Excel
import xlwings
import pythoncom
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


class ExcelOperator:
    def __init__(self, Visible: bool, ExcelInstance: Excel):
        self.Visible: bool = Visible
        self.ExcelInstance: Excel = ExcelInstance

        # If this book is already open we are going to save then close it before doing anything fancy
        try:
            Books = xlwings.books
        except Exception:
            Books = []

        for Book in Books:
            if Book.fullname == ExcelInstance.GetExcelFilePath():
                App = Book.app
                Book.save()
                Book.close()
                if len(App.books) == 0:
                    App.quit()

        pythoncom.CoInitialize()  # Required for some reason.
        self.App: xlwings.App | None = xlwings.App(visible=self.Visible, add_book=False)
        self.Book: xlwings.Book = self.App.books.open(self.ExcelInstance.ExcelFilePath)
        self.Sheet: xlwings.Sheet

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.App is not None:
            self.App.__exit__(type, value, traceback)
            self.App = None

    def __AlignArray(self, Array: list[list[any]]):  # type:ignore
        Max = max(len(i) for i in Array)
        for List in Array:
            List += [None] * (Max - len(List))

    def __AlignTuple(self, Array: tuple[tuple[any]]):  # type:ignore
        Max = max(len(i) for i in Array)
        for Tuple in Array:
            Tuple += (None,) * (Max - len(Tuple))

    @ExcelClassFunctionDecorator_ThreadLock
    def Save(self):
        self.Book.save()

    @ExcelClassFunctionDecorator_ThreadLock
    def CreateSheet(self, Name: str):
        self.Book.sheets.add(name=Name, after="Solutions")

    @ExcelClassFunctionDecorator_ThreadLock
    def DeleteSheet(self, Name: str):
        self.Book.sheets[Name].delete()

    @ExcelClassFunctionDecorator_ThreadLock
    def SelectSheet(self, Name: str):
        self.Sheet = self.Book.sheets[Name]

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadCellValue(self, Row: int, Col: int) -> any:  # type:ignore
        return self.Sheet.range((Row, Col), (Row, Col)).value

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadCellFormula(self, Row: int, Col: int) -> any:  # type:ignore
        return self.Sheet.range((Row, Col), (Row, Col)).formula

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadRangeValues(
        self,
        RowStart: int,
        ColStart: int,
        RowEnd: int,
        ColEnd: int,
    ) -> list[list[any]]:  # type:ignore
        return (
            self.Sheet.range((RowStart, ColStart), (RowEnd, ColEnd))
            .options(ndim=2)
            .value
        )  # type:ignore

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadRangeFormulas(
        self,
        RowStart: int,
        ColStart: int,
        RowEnd: int,
        ColEnd: int,
    ) -> tuple[tuple[any]]:  # type:ignore
        return (
            self.Sheet.range((RowStart, ColStart), (RowEnd, ColEnd))
            .options(ndim=2)
            .formula
        )  # type:ignore

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteCellValue(self, Row: int, Col: int, Data: any):  # type:ignore
        self.Sheet.range((Row, Col), (Row, Col)).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteCellFormula(self, Row: int, Col: int, Data: any):  # type:ignore
        self.Sheet.range((Row, Col), (Row, Col)).formula = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteRangeValues(
        self,
        RowStart: int,
        ColStart: int,
        Data: list[list[any]],  # type:ignore
    ):
        self.__AlignArray(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])

        self.Sheet.range(
            (RowStart, ColStart), (RowStart + NumRows, ColStart + NumCols)
        ).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteRangeFormulas(
        self,
        RowStart: int,
        ColStart: int,
        Data: tuple[tuple[any]],  # type:ignore
    ):
        self.__AlignTuple(Data)
        NumRows = len(Data)
        NumCols = len(Data[0])

        self.Sheet.range(
            (RowStart, ColStart), (RowStart + NumRows, ColStart + NumCols)
        ).formula = Data
