from typing import Generic, TypeVar
from dataclasses import dataclass
from ...AbstractClasses import CommandABC

T = TypeVar("T", bound="CommandABC")
S = TypeVar("S", bound="CommandABC.Response")


@dataclass
class ExceptionABC(Exception, Generic[T, S]):
    CommandInstance: T
    ResponseInstance: S

    def __post_init__(self):
        ExceptionMessage = ""
        ExceptionMessage += self.CommandInstance.ModuleName
        ExceptionMessage += ": "
        ExceptionMessage += self.CommandInstance.CommandName
        ExceptionMessage += "-> "
        ExceptionMessage += self.ResponseInstance.GetDetails()
        Exception.__init__(self, ExceptionMessage)
