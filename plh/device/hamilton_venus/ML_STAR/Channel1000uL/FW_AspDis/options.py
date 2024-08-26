from typing import Literal

from pydantic import dataclasses

from plh.device.tools import OptionsBase


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
