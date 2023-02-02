from .....Tools.AbstractClasses import ObjectABC


class Options(ObjectABC):
    def __init__(
        self, Name: str, ToolSequence: str, Sequence: str, SequencePosition: int
    ):

        self.Name: str = Name

        self.ToolSequence: str = ToolSequence

        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition

    def GetName(self) -> str:
        return self.Name
