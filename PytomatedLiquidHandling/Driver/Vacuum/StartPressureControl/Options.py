from ....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, PumpID: int, Pressure: float):

        self.Name: str = Name

        self.PumpID: int = PumpID
        self.Pressure: float = Pressure

    def GetName(self) -> str:
        return self.Name
