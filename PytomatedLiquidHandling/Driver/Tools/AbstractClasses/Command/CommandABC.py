import inspect
import os
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar, Generic, Self, TypeVar

from .....Tools.AbstractClasses import NonUniqueObjectABC

T = TypeVar("T", bound="CommandABC")
S = TypeVar("S", bound="CommandABC.Response")
CommandSelf = TypeVar("CommandSelf", bound="CommandABC")


@dataclass
class CommandABC(NonUniqueObjectABC):
    @dataclass
    class ExceptionABC(Exception, Generic[T, S]):
        CommandInstance: T
        ResponseInstance: S
        __Exceptions: ClassVar[dict[str | int, type[Self]]] = dict()

        @classmethod
        @abstractmethod
        def DetailsErrorValue(cls) -> str | int:
            raise Exception("Abstract method not implemented")

        def __init_subclass__(cls: type[Self]):
            try:
                cls.DetailsErrorValue()
            except:
                ModuleType = inspect.getmodule(cls)
                if ModuleType is None:
                    raise Exception(
                        "inspect.getmodule failed... This should never happen"
                    )
                FilePath = ModuleType.__file__

                raise Exception(
                    '"DetailsErrorValue" Function is not implemented in Exception: '
                    + cls.__name__
                    + ". FilePath: "
                    + str(FilePath)
                )
            cls.__Exceptions[cls.DetailsErrorValue()] = cls

        def __post_init__(self):
            ExceptionMessage = ""
            ExceptionMessage += self.CommandInstance.ModuleName
            ExceptionMessage += ": "
            ExceptionMessage += self.CommandInstance.CommandName
            ExceptionMessage += "-> "
            ExceptionMessage += self.ResponseInstance.GetDetails()
            Exception.__init__(self, ExceptionMessage)

    @dataclass
    class Response:
        @staticmethod
        def Decorator_ExpectedResponseProperty(DecoratedFunction):
            def inner(*args, **kwargs):
                return args[0].Properties[DecoratedFunction.__name__.replace("Get", "")]

            return inner

        Properties: dict[str, Any] = field(default_factory=dict)

        def SetProperty(self, Key: str, Value: Any):
            self.Properties[Key] = Value

        def UpdateProperties(self, Key: str, Value: Any):
            self.Properties.update({Key: Value})

        @Decorator_ExpectedResponseProperty
        def GetState(self) -> bool:
            ...

        @Decorator_ExpectedResponseProperty
        def GetDetails(self) -> str:
            ...

    @staticmethod
    def __GetCommandName(__file__: str) -> str:
        """Uses the path of the python module to extract a command name

        Args:
            __file__ (str): The path of the python module

        Returns:
            str: Command name
        """
        return os.path.basename(os.path.dirname(__file__))

    @staticmethod
    def __GetModuleName(__file__: str) -> str:
        """Uses the path of the python module to extract a module name

        Args:
            __file__ (str): The path of the python module

        Returns:
            str: Module name
        """
        Modules = list()
        Path = os.path.dirname(os.path.dirname(__file__))

        while os.path.basename(Path) != "Driver":
            Modules.append(os.path.basename(Path))
            Path = os.path.dirname(Path)

        Modules.reverse()
        Output = ""

        for Module in Modules:
            Output += Module
            Output += " "

        return Output[:-1]

    ModuleName: ClassVar[str] = "Not Set"
    CommandName: ClassVar[str] = "Not Set"

    def __post_init__(self):
        ModuleType = inspect.getmodule(type(self))
        if ModuleType is None:
            raise Exception("inspect.getmodule failed... This should never happen")
        FilePath = ModuleType.__file__

        CommandABC.ModuleName = CommandABC.__GetModuleName(str(FilePath))
        CommandABC.CommandName = CommandABC.__GetCommandName(str(FilePath))

    @dataclass
    class UnhandledException(ExceptionABC[CommandSelf, Response]):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "__UnhandledException"
