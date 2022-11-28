from ....Tools.Command.Command import Command
from .PlacePlateOptions import PlacePlateOptions


class PlacePlateCommand(Command):
    def __init__(self, Name: str, OptionsInstance: PlacePlateOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: PlacePlateOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Transport Gripper"

    def GetCommandName(self) -> str:
        return "Place Plate"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
