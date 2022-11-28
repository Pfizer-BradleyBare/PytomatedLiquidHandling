from .....Tools.AbstractClasses import ObjectABC


class InitializeOptions(ObjectABC):
    def __init__(self, Name: str, TipSequence: str, WasteSequence: str):

        self.Name: str = Name

        self.TipSequence: str = TipSequence
        self.WasteSequence: str = WasteSequence

    def GetName(self) -> str:
        return self.Name
