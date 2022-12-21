from typing import Callable

from ....Tools.Command.Command import Command
from .TipsAvailableOptions import TipsAvailableOptions


class TipsAvailableCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: TipsAvailableOptions,
        CallbackFunction: Callable[[tuple], None] | None = None,
        CallbackArgs: tuple | None = None,
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
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
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
