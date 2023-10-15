from dataclasses import dataclass
from typing import Literal
from .....Tools.AbstractClasses import OptionsABC
from enum import Enum


@dataclass(kw_only=True)
class Options(OptionsABC):
    Sequence: str
    PositionID: str


@dataclass(kw_only=True)
class ListedOptions(list[Options]):
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
