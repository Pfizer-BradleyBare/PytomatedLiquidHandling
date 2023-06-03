from typing import Generic, TypeVar

from ...AbstractClasses import CommandABC

T = TypeVar("T", bound="CommandABC")
S = TypeVar("S", bound="CommandABC.Response")


class ExceptionABC(Exception, Generic[T, S]):
    def __init__(self, CommandInstance: T, ResponseInstance: S):
        self.CommandInstance: T = CommandInstance
        self.ResponseInstance: S = ResponseInstance
        ExceptionMessage = ""
        ExceptionMessage += CommandInstance.ModuleName
        ExceptionMessage += ": "
        ExceptionMessage += CommandInstance.CommandName
        ExceptionMessage += "-> "
        ExceptionMessage += ResponseInstance.GetDetails()
        Exception.__init__(self, ExceptionMessage)
