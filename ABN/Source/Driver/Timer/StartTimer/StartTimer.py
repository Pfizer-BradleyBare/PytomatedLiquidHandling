from typing import Callable

from ...Tools.Command.Command import Command
from .StartTimerOptions import StartTimerOptions


class StartTimerCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: StartTimerOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: StartTimerOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Timer"

    def GetCommandName(self) -> str:
        return "Start Timer"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
