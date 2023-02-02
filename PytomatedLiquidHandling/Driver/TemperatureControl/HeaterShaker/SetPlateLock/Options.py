from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, HandleID: int, PlateLockState: int):

        self.Name: str = Name

        self.HandleID: int = HandleID
        self.PlateLockState: int = PlateLockState

    def GetName(self) -> str:
        return self.Name
