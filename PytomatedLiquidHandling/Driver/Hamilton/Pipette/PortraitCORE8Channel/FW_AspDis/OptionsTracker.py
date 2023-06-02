from enum import Enum
from typing import Literal

from .....Tools.AbstractClasses import OptionsTrackerABC
from .Options import Options


class OptionsTracker(OptionsTrackerABC[Options]):
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

    def __init__(
        self,
        *,
        LLDSearchHeight: int,
        LiquidClass: str,
        SettlingTimeStoppable: YesNoOptions,
        Aspirate: YesNoOptions,
        AspirateTraverseBeforeAspirate: YesNoOptions,
        AspirateTraverseAfterAspirate: YesNoOptions,
        AspirateFixHeightFromBottom: float,
        AspirateRetractDistanceForTransportAir: int,
        AspirateVolume: float,
        AspirateAdditionalSettlingTime: int,
        AspirateBlowoutVolume: float | Literal[""],
        Dispense: YesNoOptions,
        DispenseTraverseBeforeDispense: YesNoOptions,
        DispenseTraverseAfterDispense: YesNoOptions,
        DispenseFixHeightFromBottom: float,
        DispenseVolume: float,
        DispenseAdditionalSettlingTime: int,
        DispenseBlowoutVolume: float | Literal[""],
    ):
        self.LLDSearchHeight: int = LLDSearchHeight
        self.LiquidClass: str = LiquidClass
        self.SettlingTimeStoppable: int = SettlingTimeStoppable.value

        self.Aspirate: int = Aspirate.value
        self.AspirateTraverseBeforeAspirate: int = AspirateTraverseBeforeAspirate.value
        self.AspirateTraverseAfterAspirate: int = AspirateTraverseAfterAspirate.value
        self.AspirateFixHeightFromBottom: float = AspirateFixHeightFromBottom
        self.AspirateRetractDistanceForTransportAir: int = (
            AspirateRetractDistanceForTransportAir
        )
        self.AspirateVolume: float = AspirateVolume
        self.AspirateAdditionalSettlingTime: int = AspirateAdditionalSettlingTime
        self.AspirateBlowoutVolume: float | str = AspirateBlowoutVolume

        self.Dispense: int = Dispense.value
        self.DispenseTraverseBeforeDispense: int = DispenseTraverseBeforeDispense.value
        self.DispenseTraverseAfterDispense: int = DispenseTraverseAfterDispense.value
        self.DispenseFixHeightFromBottom: float = DispenseFixHeightFromBottom
        self.DispenseVolume: float = DispenseVolume
        self.DispenseAdditionalSettlingTime: int = DispenseAdditionalSettlingTime
        self.DispenseBlowoutVolume: float | str = DispenseBlowoutVolume
