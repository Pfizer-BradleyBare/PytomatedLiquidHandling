from typing import Callable

from ....Tools.Command.Command import Command
from .LoadOptions import LoadOptions


class LoadCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: LoadOptions,
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
        self.OptionsInstance: LoadOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Deck Loading Dialog Plate5Position"

    def GetCommandName(self) -> str:
        return "Load"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
