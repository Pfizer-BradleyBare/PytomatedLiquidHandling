from enum import Enum

from .....Tools.AbstractClasses import OptionsABC


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
