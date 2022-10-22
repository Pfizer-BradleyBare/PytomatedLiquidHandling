from .....AbstractClasses import ObjectABC


class WellFactor(ObjectABC):
    def __init__(self, WellNumber: int, Factor: float):
        self.WellNumber: int = WellNumber
        self.Factor: float = Factor

    def GetName(self) -> int:
        return self.WellNumber

    def GetFactor(self) -> float:
        return self.Factor
