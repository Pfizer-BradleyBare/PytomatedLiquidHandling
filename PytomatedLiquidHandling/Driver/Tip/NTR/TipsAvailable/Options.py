from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        TipSequence: str,
        GeneratedRackWasteSequence: str,
        GripperSequence: str,
        NumPositions: int,
    ):

        self.TipSequence: str = TipSequence
        self.GeneratedRackWasteSequence: str = GeneratedRackWasteSequence
        self.GripperSequence: str = GripperSequence
        self.NumPositions: int = NumPositions
