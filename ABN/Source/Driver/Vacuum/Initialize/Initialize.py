from typing import Callable

from ...Tools.Command.Command import Command
from .InitializeOptions import InitializeOptions


class InitializeCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: InitializeOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: InitializeOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
