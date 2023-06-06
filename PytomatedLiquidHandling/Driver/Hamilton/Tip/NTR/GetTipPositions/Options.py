from .....Tools.AbstractClasses import OptionsABC
from dataclasses import dataclass


@dataclass(kw_only=True)
class Options(OptionsABC):
    TipSequence: str
    GeneratedRackWasteSequence: str
    GripperSequence: str
    NumPositions: int
