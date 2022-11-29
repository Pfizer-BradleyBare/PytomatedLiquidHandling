from ....Tools.Command.Command import Command
from .GetShakingSpeedOptions import GetShakingSpeedOptions


class StopShakeControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: GetShakingSpeedOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: GetShakingSpeedOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Stop Shake Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
