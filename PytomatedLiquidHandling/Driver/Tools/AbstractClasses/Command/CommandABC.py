import os
from abc import abstractmethod
from typing import Any, Self

from .....Tools.AbstractClasses import NonUniqueObjectABC
from ...AbstractClasses import ExceptionABC


class CommandABC(NonUniqueObjectABC):
    ClassFilePath: str

    class Exception_Unhandled(ExceptionABC):
        ...

    class Response:
        @staticmethod
        def Decorator_ExpectedSuccessResponseProperty(DecoratedFunction):
            def inner(*args, **kwargs):
                return args[0].Properties[DecoratedFunction.__name__.replace("Get", "")]

            inner.Decorated_ExpectedSuccessResponseProperty = True
            return inner

        @staticmethod
        def Decorator_ExpectedErrorResponseProperty(DecoratedFunction):
            def inner(*args, **kwargs):
                return args[0].Properties[DecoratedFunction.__name__.replace("Get", "")]

            inner.Decorated_ExpectedErrorResponseProperty = True
            return inner

        @classmethod
        def GetExpectedSuccessResponseProperties(cls) -> list[str]:
            Out = list()

            for Name in dir(cls):
                if hasattr(
                    getattr(cls, Name), "Decorated_ExpectedSuccessResponseProperty"
                ):
                    Out.append(Name.replace("Get", ""))

            return Out

        @classmethod
        def GetExpectedErrorResponseProperties(cls) -> list[str]:
            Out = list()

            for Name in dir(cls):
                if hasattr(
                    getattr(cls, Name), "Decorated_ExpectedErrorResponseProperty"
                ):
                    Out.append(Name.replace("Get", ""))

            return Out

        def __init__(self, Properties: dict[str, Any]):
            self.Properties: dict[str, Any] = Properties

        def SetProperty(self, Key: str, Value: Any):
            self.Properties[Key] = Value

        def UpdateProperties(self, Key: str, Value: Any):
            self.Properties.update({Key: Value})

        @Decorator_ExpectedSuccessResponseProperty
        @Decorator_ExpectedErrorResponseProperty
        def GetState(self) -> bool:
            ...

        @Decorator_ExpectedSuccessResponseProperty
        @Decorator_ExpectedErrorResponseProperty
        def GetDetails(self) -> str:
            ...

    @staticmethod
    def Decorator_Command(__file__: str):
        def InnerDecorator(DecoratedClass):
            DecoratedClass.ClassFilePath = __file__
            return DecoratedClass

        return InnerDecorator

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

    def __init__(self, Identifier: str):
        NonUniqueObjectABC.__init__(self, Identifier)
        self.ModuleName: str = CommandABC.__GetModuleName(self.ClassFilePath)
        self.CommandName: str = CommandABC.__GetCommandName(self.ClassFilePath)

    @abstractmethod
    def ParseResponseRaiseExceptions(self, ResponseInstance: Response):
        ...
