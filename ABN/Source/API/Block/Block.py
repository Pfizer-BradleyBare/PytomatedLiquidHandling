from ...AbstractClasses import ObjectABC


class Block(ObjectABC):
    def __init__(
        self, Title: str, Row: int, Col: int, Context: str, Params: dict[str, any]
    ):
        self.Title: str = Title
        self.Row: int = None
        self.Col: int = None
        self.Context: str = None
        self.Parameter: dict[str, any] = {}

    def __str__(self):
        print("Step Title:", self.Title)
        print("Step Coordinates: (", self.Row, ",", self.Col, ")")
        print("Parent Plate:", self.GetParentPlateName())
        print("Context:", self.Context)
        return "Step Parameters: " + str(self.Parameters)

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.Row == other.Row and self.Col == other.Col
        # Row and Col in excel file is always unique so we can find step using only those parameters.

    def GetName(self) -> str:
        return self.Title

    def GetTitle(self) -> str:
        return self.Title

    def GetCoordinates(self) -> tuple[int, int]:
        return (self.Row, self.Col)

    def GetParentPlateName(self) -> str:
        return self.Context[self.Context.rfind(":") + 1 :]

    def GetContext(self) -> str:
        return self.Context

    def GetParentContext(self) -> str:
        return self.Context[: self.Context.rfind(":")]

    def GetParameters(self) -> dict[str, any]:
        return self.Parameters
