from ...Tools.Command.Command import Command
from .GetPressureOptions import GetPressureOptions


class GetPressureCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: GetPressureOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: GetPressureOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Get Pressure"

    def GetResponseKeys(self) -> list[str]:
        return ["Pressure"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
