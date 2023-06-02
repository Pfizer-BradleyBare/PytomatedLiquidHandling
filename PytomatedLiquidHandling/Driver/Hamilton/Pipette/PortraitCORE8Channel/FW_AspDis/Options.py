from enum import Enum
from typing import Literal

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(self, *, Sequence: str, SequencePosition: int):
        self.Sequence: str = Sequence
        self.SequencePosition: int = SequencePosition
