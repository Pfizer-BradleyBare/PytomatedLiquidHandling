from ....Tools.AbstractClasses import ExceptionABC, UnhandledException
from typing import TypeVar
from ..HamiltonCommand import HamiltonCommandABC
from ..HamiltonResponse import HamiltonResponseABC

HamiltonCommandABCType = TypeVar("HamiltonCommandABCType", bound=HamiltonCommandABC)
HamiltonResponseABCType = TypeVar("HamiltonResponseABCType", bound=HamiltonResponseABC)


class NoOptionsInTracker(ExceptionABC[HamiltonCommandABCType, HamiltonResponseABCType]):
    def __init_subclass__(cls) -> None:
        cls.ErrorCode = -65535
