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
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: InitializeOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Closed Container FlipTube"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
