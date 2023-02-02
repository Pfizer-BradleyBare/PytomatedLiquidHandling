from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, HandleID: int, Temperature: float):

        self.Name: str = Name

        self.HandleID: int = HandleID
        self.Temperature: float = Temperature

    def GetName(self) -> str:
        return self.Name
