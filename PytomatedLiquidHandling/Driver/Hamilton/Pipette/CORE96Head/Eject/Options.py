from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        Sequence: str,
    ):
        self.Sequence: str = Sequence
