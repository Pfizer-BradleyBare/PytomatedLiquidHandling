from typing import Callable

from ....Tools.Command.Command import Command
from .TipsRemainingOptions import TipsRemainingOptions


class TipsRemainingCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: TipsRemainingOptions,
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
        self.OptionsInstance: TipsRemainingOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Tips Remaining"

    def GetResponseKeys(self) -> list[str]:
        return ["NumRemaining"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
