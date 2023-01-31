from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, HandleID: str):

        self.Name: str = Name

        self.HandleID: str = HandleID

    def GetName(self) -> str:
        return self.Name
