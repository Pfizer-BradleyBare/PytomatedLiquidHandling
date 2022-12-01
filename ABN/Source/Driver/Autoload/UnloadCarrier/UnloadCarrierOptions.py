from ....Tools.AbstractClasses import ObjectABC


class UnloadCarrierOptions(ObjectABC):
    def __init__(self, Name: str, Sequence: str):

        self.Name: str = Name

        self.Sequence: str = Sequence

    def GetName(self) -> str:
        return self.Name
