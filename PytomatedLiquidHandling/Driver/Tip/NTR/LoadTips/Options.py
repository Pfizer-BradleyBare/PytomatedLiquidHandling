from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(
        self, Name: str, TipSequence: str, RackWasteSequence: str, GripperSequence: str
    ):

        self.Name: str = Name

        self.TipSequence: str = TipSequence
        self.RackWasteSequence: str = RackWasteSequence
        self.GripperSequence: str = GripperSequence

        self.LoadingText: str = "Load NTR Tips"

    def GetName(self) -> str:
        return self.Name
