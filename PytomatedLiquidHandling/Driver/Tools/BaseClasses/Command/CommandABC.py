import inspect
import os
from typing import ClassVar

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class CommandABC:
    """Base dataclass for all commands. All commands must be a dataclass with ```kw_only=True``` for consistency sake.

    Commands should be contained in a folder with 4 files below. These 4 files make up a single command that can be executed on your backend:.
    - __init__.py
    - Command.py
    - Options.py
    - Response.py
    """

    Identifier: str = "N/A"
    """All commands have an optional identifier. Provided for more logging context."""

    ModuleName: ClassVar[str]
    """This is the path from the ```Driver``` folder. This is autodetermined upon dataclass creation."""

    CommandName: ClassVar[str]
    """This is the folder name where your 4 files are contained. This is autodetermined upon dataclass creation."""

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

    def __post_init__(self):
        ModuleType = inspect.getmodule(type(self))
        if ModuleType is None:
            raise RuntimeError("inspect.getmodule failed... This should never happen")
        FilePath = ModuleType.__file__

        CommandABC.ModuleName = CommandABC.__GetModuleName(str(FilePath))
        CommandABC.CommandName = CommandABC.__GetCommandName(str(FilePath))
