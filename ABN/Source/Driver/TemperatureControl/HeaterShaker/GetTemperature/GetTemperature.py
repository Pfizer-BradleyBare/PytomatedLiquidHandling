from typing import Callable

from ....Tools.Command.Command import Command
from .GetTemperatureOptions import GetTemperatureOptions


class GetTemperatureCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: GetTemperatureOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: GetTemperatureOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Get Temperature"

    def GetResponseKeys(self) -> list[str]:
        return ["Temperature"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
