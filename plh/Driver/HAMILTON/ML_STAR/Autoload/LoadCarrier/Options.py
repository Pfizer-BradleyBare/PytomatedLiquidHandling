import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    class LabwarePositionsOptions(Enum):
        ReadPresentLabware = "?"
        ReadAllPositions = "*"
        ReadNone = ""

    LabwareID: str
    BarcodeFilePath: str
    LabwarePositions: LabwarePositionsOptions = (
        LabwarePositionsOptions.ReadPresentLabware
    )
