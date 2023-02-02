from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, HandleID: int, ShakingSpeed: int):

        self.Name: str = Name

        self.HandleID: int = HandleID
        self.ShakingSpeed: int = ShakingSpeed

    def GetName(self) -> str:
        return self.Name
