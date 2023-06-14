from dataclasses import dataclass
from enum import Enum

from ....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class LabwareImageOptions(Enum):
        Biorad200uL96WellPlate = "Biorad200uL96WellPlate"

    CarrierPosition: int
    LabwareImage: LabwareImageOptions
    LabwareSupportingText: str
    LabwareExtendedInformation: str | None = None
