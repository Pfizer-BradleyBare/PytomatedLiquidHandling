from typing import Callable

from ...Tools.Command.Command import Command
from .StartPressureControlOptions import StartPressureControlOptions


class StartPressureControlCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: StartPressureControlOptions,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple | None = None,
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: StartPressureControlOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Start Pressure Control"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
