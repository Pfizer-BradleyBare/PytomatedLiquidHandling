from .....Tools.AbstractClasses import ObjectABC


class GetTipSequencePositionsOptions(ObjectABC):
    def __init__(
        self,
        Name: str,
        TipSequence: str,
        GeneratedRackWasteSequence: str,
        GripperSequence: str,
        NumPositions: int,
    ):

        self.Name: str = Name

        self.TipSequence: str = TipSequence
        self.GeneratedRackWasteSequence: str = GeneratedRackWasteSequence
        self.GripperSequence: str = GripperSequence
        self.NumPositions: int = NumPositions

    def GetName(self) -> str:
        return self.Name
