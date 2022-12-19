from .....Tools.AbstractClasses import ObjectABC


class WellSequence(ObjectABC):
    def __init__(self, WellNumber: int, Sequence: int):
        self.WellNumber: int = WellNumber
        self.Sequence: int = Sequence

    def GetName(self) -> int:
        return self.WellNumber

    def GetSequence(self) -> int:
        return self.Sequence
