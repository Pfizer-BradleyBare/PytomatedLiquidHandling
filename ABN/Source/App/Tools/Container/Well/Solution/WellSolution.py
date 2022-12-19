from ......Tools.AbstractClasses import ObjectABC


class WellSolution(ObjectABC):
    def __init__(self, Name: str, Volume: float):
        self.Name: str = Name
        self.Volume: float = Volume

    def GetName(self) -> str:
        return self.Name

    def GetVolume(self) -> float:
        return self.Volume
