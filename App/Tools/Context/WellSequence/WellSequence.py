from PytomatedLiquidHandling.Tools.AbstractClasses import ObjectABC


class WellSequence(ObjectABC):
    def __init__(self, WellNumber: int, SequencePosition: int):
        self.WellNumber: int = WellNumber
        self.SequencePosition: int = SequencePosition

    def GetName(self) -> int:
        return self.WellNumber
