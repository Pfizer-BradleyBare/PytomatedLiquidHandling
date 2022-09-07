from ....AbstractClasses import ObjectABC
from ....Tools import Excel
from abc import abstractmethod

_AvailableBlocks = dict()


def ClassDecorator_AvailableBlock(DecoratedClass):
    _AvailableBlocks[DecoratedClass.__name__] = DecoratedClass
    # We are creating a decorator to simplify class creation without messy if else statements.
    return DecoratedClass


class Block(ObjectABC):
    def __init__(
        self,
        ExcelInstance: Excel,
        Row: int,
        Col: int,
    ):
        self.ExcelInstance: Excel = ExcelInstance
        self.Row: int = Row
        self.Col: int = Col

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.Row == other.Row and self.Col == other.Col
        # Row and Col in excel file is always unique so we can find step using only those parameters.

    def GetRow(self) -> int:
        return self.Row

    def GetCol(self) -> int:
        return self.Col

    @abstractmethod
    def Process(self, WorkbookInstance, HalInstance):
        raise NotImplementedError


def BlockObjectCreationWrapper(
    ExcelInstance: Excel, Title: str, Row: int, Col: int
) -> Block:
    return _AvailableBlocks[Title.replace(" ", "")](ExcelInstance, Row, Col)
