from ...Server.Globals import LOG
from .ExcelHandle import ExcelHandle


def ExcelClassFunctionDecorator_ThreadLock(DecoratedFunction):
    def inner(*args, **kwargs):
        LOG.debug("Excel Function: " + DecoratedFunction.__name__)

        if args[0].ExcelHandleInstance.IsValid() is True:
            Result = DecoratedFunction(*args, **kwargs)
        else:
            LOG.critical("Excel handle is not valid! No action performed")
            Result = None

        LOG.debug("Excel Function: " + DecoratedFunction.__name__)
        return Result

    return inner


class Excel:
    def __init__(self, ExcelFilePath: str):
        self.ExcelFilePath: str = ExcelFilePath
        self.ExcelHandleInstance: ExcelHandle = ExcelHandle(False)
        self.SheetString: str

    def AttachHandle(self, ExcelHandleInstance: ExcelHandle):
        self.ExcelHandleInstance = ExcelHandleInstance
        self.ExcelHandleInstance.OpenBook(self.ExcelFilePath)

    def GetExcelFilePath(self) -> str:
        return self.ExcelFilePath

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
        self.ExcelHandleInstance.GetBook().save()

    @ExcelClassFunctionDecorator_ThreadLock
    def CreateSheet(self, Name: str):
        self.ExcelHandleInstance.GetBook().sheets.add(name=Name, after="Solutions")

    @ExcelClassFunctionDecorator_ThreadLock
    def DeleteSheet(self, Name: str):
        self.ExcelHandleInstance.GetBook().sheets[Name].delete()

    def SelectSheet(self, Name: str):
        self.SheetString = Name

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadCellValue(self, Row: int, Col: int) -> any:  # type:ignore
        return (
            self.ExcelHandleInstance.GetBook()
            .sheets[self.SheetString]
            .range((Row, Col), (Row, Col))
            .value
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadCellFormula(self, Row: int, Col: int) -> any:  # type:ignore
        return (
            self.ExcelHandleInstance.GetBook()
            .sheets[self.SheetString]
            .range((Row, Col), (Row, Col))
            .formula
        )

    @ExcelClassFunctionDecorator_ThreadLock
    def ReadRangeValues(
        self,
        RowStart: int,
        ColStart: int,
        RowEnd: int,
        ColEnd: int,
    ) -> list[list[any]]:  # type:ignore
        return (
            self.ExcelHandleInstance.GetBook()
            .sheets[self.SheetString]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
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
            self.ExcelHandleInstance.GetBook()
            .sheets[self.SheetString]
            .range((RowStart, ColStart), (RowEnd, ColEnd))
            .options(ndim=2)
            .formula
        )  # type:ignore

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteCellValue(self, Row: int, Col: int, Data: any):  # type:ignore
        self.ExcelHandleInstance.GetBook().sheets[self.SheetString].range(
            (Row, Col), (Row, Col)
        ).value = Data

    @ExcelClassFunctionDecorator_ThreadLock
    def WriteCellFormula(self, Row: int, Col: int, Data: any):  # type:ignore
        self.ExcelHandleInstance.GetBook().sheets[self.SheetString].range(
            (Row, Col), (Row, Col)
        ).formula = Data

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

        self.ExcelHandleInstance.GetBook().sheets[self.SheetString].range(
            (RowStart, ColStart), (RowStart + NumRows - 1, ColStart + NumCols - 1)
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

        self.ExcelHandleInstance.GetBook().sheets[self.SheetString].range(
            (RowStart, ColStart), (RowStart + NumRows - 1, ColStart + NumCols - 1)
        ).formula = Data
