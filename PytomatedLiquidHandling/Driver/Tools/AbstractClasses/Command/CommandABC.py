import inspect
import os
from dataclasses import dataclass, field
from typing import Any, ClassVar


@dataclass(kw_only=True)
class CommandABC:
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
    Identifier: str = field(default="N/A")

    def __post_init__(self):
        ModuleType = inspect.getmodule(type(self))
        if ModuleType is None:
            raise RuntimeError("inspect.getmodule failed... This should never happen")
        FilePath = ModuleType.__file__

        CommandABC.ModuleName = CommandABC.__GetModuleName(str(FilePath))
        CommandABC.CommandName = CommandABC.__GetCommandName(str(FilePath))
