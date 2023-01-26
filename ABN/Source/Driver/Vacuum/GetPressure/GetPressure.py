from typing import Callable

from ...Tools.Command.Command import Command
from .GetPressureOptions import GetPressureOptions


class GetPressureCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: GetPressureOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: GetPressureOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Get Pressure"

    def GetResponseKeys(self) -> list[str]:
        return ["Pressure"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
