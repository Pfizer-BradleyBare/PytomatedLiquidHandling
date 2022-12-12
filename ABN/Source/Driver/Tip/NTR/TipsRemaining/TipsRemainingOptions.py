from .....Tools.AbstractClasses import ObjectABC


class TipsRemainingOptions(ObjectABC):
    def __init__(self, Name: str, TipSequence: str):

        self.Name: str = Name

        self.TipSequence: str = TipSequence

    def GetName(self) -> str:
        return self.Name
