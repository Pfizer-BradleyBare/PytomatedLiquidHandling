from enum import Enum
from typing import Literal

from pydantic import dataclasses

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


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class OptionsList(list[Options]):
    LLDSearchHeight: int
    LiquidClass: str
    SettlingTimeStoppable: bool
    Aspirate: bool
    AspirateTraverseBeforeAspirate: bool
    AspirateTraverseAfterAspirate: bool
    AspirateFixHeightFromBottom: float
    AspirateRetractDistanceForTransportAir: int
    AspirateVolume: float
    AspirateAdditionalSettlingTime: int
    AspirateBlowoutVolume: float | Literal[""]
    Dispense: bool
    DispenseTraverseBeforeDispense: bool
    DispenseTraverseAfterDispense: bool
    DispenseFixHeightFromBottom: float
    DispenseVolume: float
    DispenseAdditionalSettlingTime: int
    DispenseBlowoutVolume: float | Literal[""]
