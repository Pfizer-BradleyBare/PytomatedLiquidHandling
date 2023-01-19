from typing import Callable

from ....Tools.Command.Command import Command
from .TipsAvailableOptions import TipsAvailableOptions


class TipsAvailableCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: TipsAvailableOptions,
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
        self.OptionsInstance: TipsAvailableOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Tips Available"

    def GetResponseKeys(self) -> list[str]:
        return ["TipPosition"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
