from ....Tools.Command.Command import Command
from .StopTemperatureControlOptions import StopTemperatureControlOptions


class StopTemperatureControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StopTemperatureControlOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: StopTemperatureControlOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterCooler"

    def GetCommandName(self) -> str:
        return "Stop Temperature Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
