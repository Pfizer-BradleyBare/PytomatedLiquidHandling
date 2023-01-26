from typing import Callable

from ....Tools.Command.Command import Command
from .PlacePlateOptions import PlacePlateOptions


class PlacePlateCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: PlacePlateOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: PlacePlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport IPG"

    def GetCommandName(self) -> str:
        return "Place Plate"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
