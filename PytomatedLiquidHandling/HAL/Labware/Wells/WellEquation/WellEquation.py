from .....Tools.AbstractClasses import UniqueObjectABC


class WellEquation(UniqueObjectABC):
    def __init__(self, SegmentHeight: float, SegmentEquation: str):
        self.Height = SegmentHeight
        self.Equation = SegmentEquation

    def GetName(self) -> float:
        return self.Height
