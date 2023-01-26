from typing import Callable

from ....Tools.Command.Command import Command
from .TipsRemainingOptions import TipsRemainingOptions


class TipsRemainingCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: TipsRemainingOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
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

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
