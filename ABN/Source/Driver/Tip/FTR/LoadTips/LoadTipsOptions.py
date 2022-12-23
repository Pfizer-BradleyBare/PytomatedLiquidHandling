from .....Tools.AbstractClasses import ObjectABC


class LoadTipsOptions(ObjectABC):
    def __init__(self, Name: str, TipSequence: str):

        self.Name: str = Name

        self.TipSequence: str = TipSequence

        self.LoadingText: str = "Load FTR Tips"

    def GetName(self) -> str:
        return self.Name
