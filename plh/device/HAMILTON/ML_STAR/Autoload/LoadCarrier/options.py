from pydantic import dataclasses

from plh.device.HAMILTON.complex_inputs import LabwarePositionsOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    BarcodeFilePath: str = "barcode_1.txt"
    LabwarePositions: LabwarePositionsOptions = (
        LabwarePositionsOptions.ReadPresentLabware
    )
