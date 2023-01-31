from ....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, PumpID: int):

        self.Name: str = Name

        self.PumpID: int = PumpID

    def GetName(self) -> str:
        return self.Name
