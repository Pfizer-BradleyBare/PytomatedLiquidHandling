import time
from dataclasses import dataclass, field
from typing import Any, Callable

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class Timer(UniqueObjectABC):
    WaitTime: float
    EndTime: float = field(init=False)
    Kill: bool = field(init=False, default=False)
    CallbackFunction: Callable[..., None]
    CallbackArgs: tuple[Any]

    def __post_init__(self):
        self.EndTime = time.time() + self.WaitTime

    def GetRemainingTime(self) -> float:
        return self.EndTime - time.time()

    def IsExpired(self) -> bool:
        return time.time() >= self.EndTime or self.Kill == True

    def ForceExpiration(self):
        self.Kill = True

    def ExecuteCallback(self):
        self.CallbackFunction(*self.CallbackArgs)
