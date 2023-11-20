from dataclasses import dataclass
from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class LabwarePositionsOptions(Enum):
        ReadPresentLabware = "?"
        ReadAllPositions = "*"
        ReadNone = ""

    LabwareID: str
    BarcodeFilePath: str
    LabwarePositions: LabwarePositionsOptions
