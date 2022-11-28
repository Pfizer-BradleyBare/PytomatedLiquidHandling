from ....Tools.AbstractClasses import ObjectABC


class InitializeOptions(ObjectABC):
    def __init__(self, Name: str, ComPort: int):

        self.Name: str = Name

        self.ComPort: int = ComPort

    def GetName(self) -> str:
        return self.Name
