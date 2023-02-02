from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(self, Name: str, TipSequence: str, NumPositions: int):

        self.Name: str = Name

        self.TipSequence: str = TipSequence
        self.NumPositions: int = NumPositions

    def GetName(self) -> str:
        return self.Name
