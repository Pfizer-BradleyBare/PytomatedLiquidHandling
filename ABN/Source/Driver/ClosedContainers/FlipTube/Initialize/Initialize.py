from typing import Callable

from ....Tools.Command.Command import Command
from .InitializeOptions import InitializeOptions


class InitializeCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: InitializeOptions,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: InitializeOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
