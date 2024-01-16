from __future__ import annotations

import dataclasses
import inspect
import pathlib
from typing import ClassVar


@dataclasses.dataclass(kw_only=True)
class CommandBase:
    """Base dataclass for all commands. All commands must be a dataclass with ```kw_only=True``` for consistency sake.

    Commands should be contained in a folder with 4 files below. These 4 files make up a single command that can be executed on your backend:.
    - __init__.py
    - Command.py
    - Options.py
    - Response.py
    """

    identifier: str = "N/A"
    """All commands have an optional identifier. Provided for more logging context."""

    module_name: ClassVar[str]
    """This is the path from the ```Driver``` folder. This is autodetermined upon dataclass creation."""

    command_name: ClassVar[str]
    """This is the folder name where your 4 files are contained. This is autodetermined upon dataclass creation."""

    @staticmethod
    def __get_command_name(__file__: str) -> str:
        """Uses the path of the python module to extract a command name

        Args:
        ----
            __file__ (str): The path of the python module

        Returns:
        -------
            str: Command name
        """
        return pathlib.Path(__file__).parent.name

    @staticmethod
    def __get_module_name(__file__: str) -> str:
        """Uses the path of the python module to extract a module name

        Args:
        ----
            __file__ (str): The path of the python module

        Returns:
        -------
            str: Module name
        """
        modules = []
        path = pathlib.Path(__file__).parent.parent

        while path.name != "Driver":
            modules.append(path.name)
            path = path.parent

        modules.reverse()
        output = ""

        for module in modules:
            output += module
            output += " "

        return output[:-1]

    def __post_init__(self: CommandBase) -> None:
        module_type = inspect.getmodule(type(self))
        if module_type is None:
            msg = "inspect.getmodule failed... This should never happen"
            raise RuntimeError(msg)
        file_path = module_type.__file__

        CommandBase.module_name = CommandBase.__get_module_name(str(file_path))
        CommandBase.command_name = CommandBase.__get_command_name(str(file_path))
