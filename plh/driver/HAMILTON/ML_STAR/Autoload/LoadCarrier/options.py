import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class LabwarePositionsOptions(Enum):
    ReadPresentLabware = "?"
    ReadAllPositions = "*"
    ReadNone = ""


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str
    BarcodeFilePath: str = "barcode_1.txt"
    LabwarePositions: LabwarePositionsOptions = (
        LabwarePositionsOptions.ReadPresentLabware
    )
