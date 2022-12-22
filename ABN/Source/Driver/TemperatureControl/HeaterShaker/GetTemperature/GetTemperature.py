from typing import Callable

from ....Tools.Command.Command import Command
from .GetTemperatureOptions import GetTemperatureOptions


class GetTemperatureCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: GetTemperatureOptions,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
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

        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling

        OutputDict["CommandName"] = self.GetModuleName() + " -> " + self.GetName()

        return OutputDict
