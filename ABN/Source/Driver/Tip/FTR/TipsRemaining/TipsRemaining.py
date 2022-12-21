from typing import Callable

from ....Tools.Command.Command import Command
from .TipsRemainingOptions import TipsRemainingOptions


class TipsRemainingCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: TipsRemainingOptions,
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
        self.OptionsInstance: TipsRemainingOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Tips Remaining"

    def GetResponseKeys(self) -> list[str]:
        return ["NumRemaining"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
