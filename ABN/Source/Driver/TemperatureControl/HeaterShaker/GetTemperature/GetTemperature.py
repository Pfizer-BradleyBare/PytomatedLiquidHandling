from ....Tools.Command.Command import Command
from .GetTemperatureOptions import GetTemperatureOptions


class StopShakeControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: GetTemperatureOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: GetTemperatureOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Stop Shake Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
