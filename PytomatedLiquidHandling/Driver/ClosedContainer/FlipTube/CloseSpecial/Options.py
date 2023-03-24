from .....Tools.AbstractClasses import NonUniqueObjectABC


class Options(NonUniqueObjectABC):
    def __init__(self, ToolSequence: str, Sequence: str, SequencePosition: int):

        self.ToolSequence: str = ToolSequence

        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition
