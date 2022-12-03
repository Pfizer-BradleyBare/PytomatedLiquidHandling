from ....Tools.Command.Command import Command
from .GetPlateOptions import GetPlateOptions


class GetPlateCommand(Command):
    def __init__(self, Name: str, OptionsInstance: GetPlateOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: GetPlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport IPG"

    def GetCommandName(self) -> str:
        return "Get Plate"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
