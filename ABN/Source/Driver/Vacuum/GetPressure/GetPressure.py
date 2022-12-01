from ...Tools.Command.Command import Command
from .GetPressureOptions import GetPressureOptions


class StopPressureControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: GetPressureOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: GetPressureOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Stop Pressure Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)