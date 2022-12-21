from abc import abstractmethod

from ....Tools.AbstractClasses import ObjectABC
from ...Tools.Excel import Excel
from ...Tools.Tree import Node

_AvailableBlocks = dict()


def ClassDecorator_AvailableBlock(DecoratedClass):
    _AvailableBlocks[DecoratedClass.__name__] = DecoratedClass
    # We are creating a decorator to simplify class creation without messy if else statements.
    return DecoratedClass


def FunctionDecorator_ProcessFunction(DecoratedFunction):
    def inner(*args, **kwargs):

        Result = DecoratedFunction(*args, **kwargs)
        Self = args[0]
        WorkbookInstance = args[1]

        WorkbookInstance.GetContainerTracker().PlateTrackerInstance.GetObjectByName(
            Self.GetParentPlateName()
        ).BlockTrackerInstance.ManualLoad(Self)

        return Result

    return inner


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

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.GetName()) + "\n"
        for child in self.Children:
            ret += child.__repr__(level + 1)  # type:ignore
        return ret

    def GetRow(self) -> int:
        return self.Row

    def GetCol(self) -> int:
        return self.Col

    def GetContext(self) -> str:
        return self.Context

    def GetParentPlateName(self) -> str:
        return self.Context[self.Context.rfind(":") + 1 :]  # noqa203

    @abstractmethod
    # This is where actual block execution should occur
    def Preprocess(self, WorkbookInstance):
        raise NotImplementedError

    @abstractmethod
    # This is where actual block execution should occur
    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance):
        raise NotImplementedError


def BlockObjectCreationWrapper(
    ExcelInstance: Excel, Title: str, Row: int, Col: int
) -> Block:
    return _AvailableBlocks[Title.replace(" ", "")](ExcelInstance, Row, Col)
