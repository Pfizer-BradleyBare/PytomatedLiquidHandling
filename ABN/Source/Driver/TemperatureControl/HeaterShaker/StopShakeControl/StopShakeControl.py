from ....Tools.Command.Command import Command
from .StopShakeControlOptions import StopShakeControlOptions


class StopShakeControlCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: StopShakeControlOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: StopShakeControlOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Stop Shake Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
