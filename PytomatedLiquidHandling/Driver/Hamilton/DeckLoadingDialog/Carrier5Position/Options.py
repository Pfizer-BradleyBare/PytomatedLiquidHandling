from dataclasses import dataclass
from enum import Enum
from typing import Literal

from ....Tools.AbstractClasses import OptionsABC


@dataclass(kw_only=True)
class Options(OptionsABC):
    class LabwareImageOptions(Enum):
        TipNTR50uL = "TipNTR50uL"
        TipNTR300uL = "TipNTR300uL"
        TipFTR10uL = "TipFTR10uL"
        TipFTR50uL = "TipFTR50uL"
        TipFTR300uL = "TipFTR300uL"
        TipFTRSlim300uL = "TipFTRSlim300uL"
        TipFTR1000uL = "TipFTR1000uL"
        TipIMCSSizeX100 = "TipIMCSSizeX100"
        TipIMCSSizeX150 = "TipIMCSSizeX150"

        PlateBiorad200uL96Well = "PlateBiorad200uL96Well"
        PlateThermo400uL96Well = "PlateThermo400uL96Well"
        PlateThermo1200uL96Well = "PlateThermo1200uL96Well"
        PlateCorning2000uL96Well = "PlateCorning2000uL96Well"

        LidAgilentBlack = "LidAgilentBlack"

    CarrierPosition: int
    LabwareImage: LabwareImageOptions
    LabwareSupportingText: str
    LabwareExtendedInformation: str | Literal["None"] = "None"
