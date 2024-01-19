from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsBase


@dataclass
class Options(OptionsBase):
    NotificationCycleTime: int
