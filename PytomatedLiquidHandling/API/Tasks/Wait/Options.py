from dataclasses import dataclass
from typing import Any, Callable

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    Time: float
    CallbackFunction: Callable[..., None]
    CallbackArgs: tuple[Any]
