from ......Tools.AbstractClasses import NonUniqueObjectABC


class WellEquation(NonUniqueObjectABC):
    def __init__(self, SegmentHeight: float, SegmentEquation: str):
        NonUniqueObjectABC.__init__(self, "Well Equation")
        self.SegmentHeight = SegmentHeight
        self.SegmentEquation = SegmentEquation
