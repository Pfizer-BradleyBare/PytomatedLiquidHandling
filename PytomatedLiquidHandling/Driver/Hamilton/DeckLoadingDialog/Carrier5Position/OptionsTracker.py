from dataclasses import dataclass
from enum import Enum

from ....Tools.AbstractClasses import OptionsTrackerABC
from .Options import Options


@dataclass(kw_only=True)
class OptionsTracker(OptionsTrackerABC[Options]):
    class Carrier3DImageOptions(Enum):
        FTR5Position3D = "FTR5Position3D"

    class Carrier2DImageOptions(Enum):
        FTR5Position2D = "FTR5Position2D"

    DialogTitleText: str = "Please follow the instructions to load / unload the carrier with labware at the correct position(s). Use the instructions below for guidance."
    Step1Text: str = "1. Confirm a carrier was removed from the deck at the correct track number.\nNOTE: If you do not have an autoload you will need to remove the carrier manually."
    Step2Text: str = "2. Place the labware into the correct position(s) on the carrier using the guidance below. If labware is already present, be sure to check the extra information."
    CarrierSupportingText: str = "Carrier Name: <Carrier Name>\nCarrier Track Number Start: <Number>\nCarrier Track Number End: <Number>"
    Carrier3DImage: Carrier3DImageOptions
    Carrier2DImage: Carrier2DImageOptions
