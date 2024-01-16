import dataclasses
from enum import Enum
from typing import Literal

from plh.driver.tools import OptionsBase


class ModeOptions(Enum):
    Aspiration = 0
    ConsequtiveAspiration = 1
    AspirateAll = 2


class LLDOptions(Enum):
    Off = 0
    VeryHigh = 1
    High = 2
    Medium = 3
    Low = 4
    FromLabwareDefinition = 5


class YesNoOptions(Enum):
    No = 0
    Yes = 1


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    LLDSearchHeight: int
    LiquidClass: str
    SettlingTimeStoppable: YesNoOptions
    Aspirate: YesNoOptions
    AspirateTraverseBeforeAspirate: YesNoOptions
    AspirateTraverseAfterAspirate: YesNoOptions
    AspirateFixHeightFromBottom: float
    AspirateRetractDistanceForTransportAir: int
    AspirateVolume: float
    AspirateAdditionalSettlingTime: int
    AspirateBlowoutVolume: float | Literal[""]
    Dispense: YesNoOptions
    DispenseTraverseBeforeDispense: YesNoOptions
    DispenseTraverseAfterDispense: YesNoOptions
    DispenseFixHeightFromBottom: float
    DispenseVolume: float
    DispenseAdditionalSettlingTime: int
    DispenseBlowoutVolume: float | Literal[""]
