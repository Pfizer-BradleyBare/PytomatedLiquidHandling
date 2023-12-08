from enum import Enum
from typing import Literal

from pydantic import BaseModel, dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
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


class ListedOptions(list[Options], BaseModel):
    class Carrier3DImageOptions(Enum):
        Carrier5PositionFTR3D = "Carrier5PositionFTR3D"
        Carrier5PositionPlate3D = "Carrier5PositionPlate3D"

    class Carrier2DImageOptions(Enum):
        Carrier5PositionFTR2D = "Carrier5PositionFTR2D"
        Carrier5PositionPlate2D = "Carrier5PositionPlate2D"

    DialogTitleText: str = "Please follow the instructions to load / unload the carrier with labware at the correct position(s). Use the instructions below for guidance."
    Step1Text: str = "1. Confirm a carrier was removed from the deck at the correct track number.\nNOTE: If you do not have an autoload you will need to remove the carrier manually."
    Step2Text: str = "2. Place the labware into the correct position(s) on the carrier using the guidance below. If labware is already present, be sure to check the extra information."
    CarrierSupportingText: str = "Carrier Name: <Carrier Name>\nCarrier Track Number Start: <Number>\nCarrier Track Number End: <Number>"
    Carrier3DImage: Carrier3DImageOptions
    Carrier2DImage: Carrier2DImageOptions
