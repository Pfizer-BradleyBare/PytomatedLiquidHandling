from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    NotificationCycleTime: int
