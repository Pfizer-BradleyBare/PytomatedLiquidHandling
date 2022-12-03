from ...Tools.Command.Command import Command
from .StartTimerOptions import StartTimerOptions


class StartTimerCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: StartTimerOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: StartTimerOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Timer"

    def GetCommandName(self) -> str:
        return "Start Timer"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
