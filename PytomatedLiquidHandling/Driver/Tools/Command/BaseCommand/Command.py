import os
from abc import abstractmethod
from threading import Event

from .....Tools.AbstractClasses import NonUniqueObjectABC
from .Tools.GetCommandName import GetCommandName
from .Tools.GetExpectedResponseProperties import GetExpectedResponseProperties
from .Tools.GetModuleName import GetModuleName


def ExpectedResponseProperty(DecoratedFunction):
    def inner(*args, **kwargs):
        if not args[0].ResponseEvent.is_set():
            raise Exception("Response not set yet. Must run command")

        return args[0].ResponseProperties[DecoratedFunction.__name__.replace("Get", "")]

    inner.Decorated_ExpectedResponseProperty = True
    return inner


def ClassDecorator_Command(__file__: str):
    def InnerDecorator(DecoratedClass):
        DecoratedClass.ClassFilePath = __file__
        return DecoratedClass

    return InnerDecorator


class Command(NonUniqueObjectABC):
    ClassFilePath: str

    def __init__(self, CustomErrorHandling: bool, UniqueIdentifier: str):
        self.UniqueIdentifier: str = UniqueIdentifier

        self.CustomErrorHandling: bool = CustomErrorHandling

        self.ModuleName: str = GetModuleName(self.ClassFilePath)
        self.CommandName: str = GetCommandName(self.ClassFilePath)
        self.ExpectedResponseProperties: list[str] = GetExpectedResponseProperties(self)

        self.ResponseEvent: Event = Event()
        self.ResponseState: bool
        self.ResponseMessage: str
        self.ResponseProperties: dict[str, any]  # type:ignore

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier

    def GetModuleName(self) -> str:
        return self.ModuleName

    def GetCommandName(self) -> str:
        return self.CommandName

    def GetID(self) -> str:
        return (
            self.GetModuleName()
            + " -> "
            + self.GetCommandName()
            + ": "
            + self.GetUniqueIdentifier()
        )

    def GetExpectedResponseProperties(self) -> list[str]:
        return self.ExpectedResponseProperties

    def Execute(self, Timeout: float | None = None):
        from ....Handler import GetHandler

        HandlerInstance = GetHandler()
        CommandTrackerInstance = HandlerInstance.CommandTrackerInstance

        CommandTrackerInstance.ManualLoad(self)

        HandlerInstance.GetLogger().info(
            "Queued %s for execution. Waiting until execution is complete or timeout if set.",
            self.GetID(),
        )

        TimeoutFlag = self.ResponseEvent.wait(Timeout)

        CommandTrackerInstance.ManualUnload(self)

        if TimeoutFlag is True:  # This means it did not timeout
            HandlerInstance.GetLogger().info("%s execution complete.", self.GetID())

            if self.CustomErrorHandling is not False:
                self.HandleErrors()
            # If response indicates a failure then we need to run error handling if it is set.
            # Most error handling will just rerun the step. FIY

        else:
            HandlerInstance.GetLogger().info(
                "%s execution timed out. Exception raised.", self.GetID()
            )
            raise Exception("Command Timed out. Uh oh!")

    def GetResponseState(self) -> bool:
        if not self.ResponseEvent.is_set():
            raise Exception("Response not set yet. Must run command")

        return self.ResponseState

    def GetResponseMessage(self) -> str:
        if not self.ResponseEvent.is_set():
            raise Exception("Response not set yet. Must run command")

        return self.ResponseMessage

    @abstractmethod
    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        ...

    @abstractmethod
    def HandleErrors(self):
        ...
