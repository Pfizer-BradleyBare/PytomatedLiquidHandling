from ....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, ComPort: int, PumpID: int):

        self.Name: str = Name

        self.ComPort: int = ComPort
        self.PumpID: int = PumpID

    def GetName(self) -> str:
        return self.Name
