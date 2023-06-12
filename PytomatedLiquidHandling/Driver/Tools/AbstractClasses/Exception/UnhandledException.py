from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar
from ..Command import CommandABC
from ..Response import ResponseABC
from .ExceptionABC import ExceptionABC

CommandABCType = TypeVar("CommandABCType", bound=CommandABC)
ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class UnhandledException(ExceptionABC[CommandABCType, ResponseABCType]):
    def __init_subclass__(cls) -> None:
        cls.ErrorCode = ""
