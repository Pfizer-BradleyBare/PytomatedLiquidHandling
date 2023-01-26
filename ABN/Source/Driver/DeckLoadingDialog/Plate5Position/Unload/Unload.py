from typing import Callable

from ....Tools.Command.Command import Command
from .UnloadOptions import UnloadOptions


class UnloadCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: UnloadOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
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

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
