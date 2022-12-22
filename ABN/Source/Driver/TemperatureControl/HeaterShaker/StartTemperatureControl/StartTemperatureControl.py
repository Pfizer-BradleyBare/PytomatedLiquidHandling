from typing import Callable

from ....Tools.Command.Command import Command
from .StartTemperatureControlOptions import StartTemperatureControlOptions


class StartTemperatureControlCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: StartTemperatureControlOptions,
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
        self.OptionsInstance: StartTemperatureControlOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Start Temperature Control"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling

        OutputDict["CommandName"] = self.GetModuleName() + " -> " + self.GetName()

        return OutputDict
