from ...Tools.Command.Command import Command
from .GetPressureOptions import GetPressureOptions


class StopPressureControlCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: GetPressureOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: GetPressureOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Stop Pressure Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
