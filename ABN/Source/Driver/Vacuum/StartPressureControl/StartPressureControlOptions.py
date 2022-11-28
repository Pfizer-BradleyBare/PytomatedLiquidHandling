from ....Tools.AbstractClasses import ObjectABC


class StartPressureControlOptions(ObjectABC):
    def __init__(self, Name: str, HandleID: int, Pressure: float):

        self.Name: str = Name

        self.HandleID: int = HandleID
        self.Pressure: float = Pressure

    def GetName(self) -> str:
        return self.Name
