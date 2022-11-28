from ...Tools.Command.Command import Command
from .StopPressureControlOptions import StopPressureControlOptions


class StopPressureControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StopPressureControlOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: StopPressureControlOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Stop Pressure Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
