from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    NotificationCycleTime: int
