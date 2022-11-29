from .....Tools.AbstractClasses import ObjectABC


class StartTemperatureControlOptions(ObjectABC):
    def __init__(self, Name: str, HandleID: str, Temperature: float):

        self.Name: str = Name

        self.HandleID: str = HandleID
        self.Temperature: float = Temperature

    def GetName(self) -> str:
        return self.Name
