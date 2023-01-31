from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str):

        self.Name: str = Name

    def GetName(self) -> str:
        return self.Name
