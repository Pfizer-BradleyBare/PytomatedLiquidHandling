from enum import Enum

from pydantic import Field

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    class YesNoOptions(Enum):
        No = 0
        Yes = 1

    class DestinationOptions(Enum):
        DeckPosition = 1
        Home = 2

    class LabwareOrientationOptions(Enum):
        PositiveYAxis = 1
        PositiveXAxis = 2
        NegativeXAxis = 3

    LabwareID: str
    Destination: DestinationOptions
    StayAtTraversalHeight: bool = True
    LabwareOrientation: LabwareOrientationOptions = (
        LabwareOrientationOptions.PositiveYAxis
    )
    SpeedPercentage: int = Field(ge=0, le=100, default=50)
    CollisionControl: YesNoOptions = YesNoOptions.Yes
