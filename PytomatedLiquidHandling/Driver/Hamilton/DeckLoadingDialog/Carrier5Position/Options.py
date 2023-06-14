from dataclasses import dataclass
from enum import Enum
from typing import Literal

from ....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class LabwareImageOptions(Enum):
        Biorad200uL96WellPlate = "Biorad200uL96WellPlate"

    CarrierPosition: int
    LabwareImage: LabwareImageOptions
    LabwareSupportingText: str
    LabwareExtendedInformation: str | Literal["None"] = "None"
    LabwareActionText: Literal["Load", "Unload", "Add To", "Take From", "Discard"]
