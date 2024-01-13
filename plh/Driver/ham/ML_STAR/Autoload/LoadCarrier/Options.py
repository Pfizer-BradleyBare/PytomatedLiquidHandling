from enum import Enum

import dataclasses

from .....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    class LabwarePositionsOptions(Enum):
        ReadPresentLabware = "?"
        ReadAllPositions = "*"
        ReadNone = ""

    LabwareID: str
    BarcodeFilePath: str
    LabwarePositions: LabwarePositionsOptions = (
        LabwarePositionsOptions.ReadPresentLabware
    )
