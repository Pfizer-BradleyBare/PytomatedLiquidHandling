from ....Tools.Command.Command import Command
from .StartTemperatureControlOptions import StartTemperatureControlOptions


class StartTemperatureControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StartTemperatureControlOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: StartTemperatureControlOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterCooler"

    def GetCommandName(self) -> str:
        return "Start Temperature Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
