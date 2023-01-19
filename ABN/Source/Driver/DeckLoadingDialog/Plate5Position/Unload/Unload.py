from typing import Callable

from ....Tools.Command.Command import Command
from .UnloadOptions import UnloadOptions


class UnloadCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: UnloadOptions,
        CustomErrorHandlingFunction: Callable[[Command], None] | None = None,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandlingFunction,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: UnloadOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Deck Loading Dialog Plate5Position"

    def GetCommandName(self) -> str:
        return "Unload"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
