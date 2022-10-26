from ....AbstractClasses import ObjectABC
from ....Tools import Excel
from ....Tools import Node
from abc import abstractmethod

_AvailableBlocks = dict()


def ClassDecorator_AvailableBlock(DecoratedClass):
    _AvailableBlocks[DecoratedClass.__name__] = DecoratedClass
    # We are creating a decorator to simplify class creation without messy if else statements.
    return DecoratedClass


class Block(ObjectABC, Node):
    def __init__(
        self,
        ExcelInstance: Excel,
        Row: int,
        Col: int,
    ):
        Node.__init__(self)
        self.ExcelInstance: Excel = ExcelInstance
        self.Row: int = Row
        self.Col: int = Col
        self.Context: str

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.Row == other.Row and self.Col == other.Col
        # Row and Col in excel file is always unique so we can find step using only those parameters.

    def GetRow(self) -> int:
        return self.Row

    def GetCol(self) -> int:
        return self.Col

    def GetContext(self) -> str:
        return self.Context

    def GetParentPlateName(self) -> str:
        return self.Context[self.Context.rfind(":") + 1 :]  # noqa203

    @abstractmethod
    # Some blocks may require preprocessing before actual execution. What is an example?
    # Preheating a heater or thermocycler before an actual incubation. That is what preprocessing is for.
    def Preprocess(self, WorkbookInstance, HalInstance):
        raise NotImplementedError

    @abstractmethod
    # This is where actual block execution should occur
    def Process(self, WorkbookInstance, HalInstance):
        raise NotImplementedError


def BlockObjectCreationWrapper(
    ExcelInstance: Excel, Title: str, Row: int, Col: int
) -> Block:
    return _AvailableBlocks[Title.replace(" ", "")](ExcelInstance, Row, Col)
