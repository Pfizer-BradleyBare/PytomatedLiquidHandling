import os
from abc import abstractmethod
from typing import Any, Self

from .....Tools.AbstractClasses import NonUniqueObjectABC


class CommandABC(NonUniqueObjectABC):
    ClassFilePath: str

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
    def HandleErrors(self):
        ...

    class Response:
        @staticmethod
        def Decorator_ExpectedResponseProperty(DecoratedFunction):
            def inner(*args, **kwargs):
                return args[0].Properties[DecoratedFunction.__name__.replace("Get", "")]

            inner.Decorated_ExpectedResponseProperty = True
            return inner

        @classmethod
        def GetExpectedResponseProperties(cls) -> list[str]:
            """Extracts the response properties, which are decorated in the class definition, from the class

            Args:
                cls (object): Any object that inherits from CommandABC.ResponseABC

            Returns:
                list[str]: A list of response properties as strings
            """
            Out = list()

            for Name in dir(cls):
                if hasattr(getattr(cls, Name), "Decorated_ExpectedResponseProperty"):
                    Out.append(Name.replace("Get", ""))

            return Out

        def __init__(self, Properties: dict[str, Any]):
            self.Properties: dict[str, Any] = Properties

        def SetProperty(self, Key: str, Value: Any):
            self.Properties[Key] = Value

        def UpdateProperties(self, Key: str, Value: Any):
            self.Properties.update({Key: Value})

        @Decorator_ExpectedResponseProperty
        def GetStatusCode(self) -> int:
            ...

        @Decorator_ExpectedResponseProperty
        def GetDetails(self) -> str:
            ...