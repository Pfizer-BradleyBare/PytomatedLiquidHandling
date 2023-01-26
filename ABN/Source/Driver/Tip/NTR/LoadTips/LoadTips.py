from typing import Callable

from ....Tools.Command.Command import Command
from .LoadTipsOptions import LoadTipsOptions


class LoadTipsCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: LoadTipsOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: LoadTipsOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Load Tips"

    def GetResponseKeys(self) -> list[str]:
        return ["GeneratedWasteSequence"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
