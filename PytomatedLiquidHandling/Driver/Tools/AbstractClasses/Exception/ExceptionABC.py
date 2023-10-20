from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from ..Command import CommandABC
from ..Response import ResponseABC

CommandABCType = TypeVar("CommandABCType", bound=CommandABC)
ResponseABCType = TypeVar("ResponseABCType", bound=ResponseABC)


@dataclass
class ExceptionABC(Exception, Generic[CommandABCType, ResponseABCType]):
    ErrorCode = ""
    CommandInstance: CommandABCType = None
    ResponseInstance: ResponseABCType = None

    # @abstractmethod
    def __init_subclass__(cls) -> None:
        ...

    def __post_init__(self):
        ExceptionMessage = ""
        ExceptionMessage += self.CommandInstance.ModuleName
        ExceptionMessage += ": "
        ExceptionMessage += self.CommandInstance.CommandName
        ExceptionMessage += "-> "
        ExceptionMessage += self.ResponseInstance.GetDetails()
        Exception.__init__(self, ExceptionMessage)
