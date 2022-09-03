from ....AbstractClasses import ObjectABC
from ....Tools import Excel


class Block(ObjectABC):
    def __init__(
        self,
        ExcelInstance: Excel,
        Title: str,
        Row: int,
        Col: int,
    ):
        self.Title: str = Title
        self.Row: int = Row
        self.Col: int = Col

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.Row == other.Row and self.Col == other.Col
        # Row and Col in excel file is always unique so we can find step using only those parameters.

    def GetName(self) -> str:
        return self.Title + " " + str((self.Row, self.Col))

    def GetTitle(self) -> str:
        return self.Title

    def GetRow(self) -> int:
        return self.Row

    def GetCol(self) -> int:
        return self.Col

    def GetParentPlateName(self) -> str:
        return self.Context[self.Context.rfind(":") + 1 :]  # noqa: E203

    def GetParentContext(self) -> str:
        return self.Context[: self.Context.rfind(":")]
