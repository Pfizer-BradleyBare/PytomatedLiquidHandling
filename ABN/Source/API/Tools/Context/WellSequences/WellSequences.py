from ....AbstractClasses import ObjectABC


class WellSequences(ObjectABC):
    def __init__(self, WellNumber: int, WellSequences: list[int]):
        self.WellNumber: int = WellNumber
        self.WellSequences: list[int] = WellSequences

    def GetName(self) -> int:
        return self.WellNumber

    def GetWellSequences(self) -> list[int]:
        return self.WellSequences
