from __future__ import annotations

from typing import Literal

from pydantic import dataclasses

from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str
    LLDSearchHeight: int
    LiquidClass: str
    SettlingTimeStoppable: bool
    LiquidFollowingDistance: int
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
