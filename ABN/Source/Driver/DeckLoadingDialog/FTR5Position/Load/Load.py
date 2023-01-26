from typing import Callable

from ....Tools.Command.Command import Command
from .LoadOptions import LoadOptions


class LoadCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: LoadOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: LoadOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Deck Loading Dialog FTR5Position"

    def GetCommandName(self) -> str:
        return "Load"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
