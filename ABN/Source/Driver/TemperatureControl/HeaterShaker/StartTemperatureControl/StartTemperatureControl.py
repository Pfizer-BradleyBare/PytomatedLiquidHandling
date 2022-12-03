from ....Tools.Command.Command import Command
from .StartTemperatureControlOptions import StartTemperatureControlOptions


class StartTemperatureControlCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: StartTemperatureControlOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: StartTemperatureControlOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Start Temperature Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
