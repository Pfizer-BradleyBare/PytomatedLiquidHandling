from ....Tools.Command.Command import Command
from .StartTemperatureControlOptions import StartTemperatureControlOptions


class GetPlateCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StartTemperatureControlOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: StartTemperatureControlOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Start Temperature Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
