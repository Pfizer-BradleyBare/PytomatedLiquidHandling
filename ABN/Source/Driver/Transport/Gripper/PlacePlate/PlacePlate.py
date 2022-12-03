from ....Tools.Command.Command import Command
from .PlacePlateOptions import PlacePlateOptions


class PlacePlateCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: PlacePlateOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: PlacePlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport Gripper"

    def GetCommandName(self) -> str:
        return "Place Plate"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
