from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, ComPort: str):

        self.Name: str = Name

        self.ComPort: str = ComPort

    def GetName(self) -> str:
        return self.Name
