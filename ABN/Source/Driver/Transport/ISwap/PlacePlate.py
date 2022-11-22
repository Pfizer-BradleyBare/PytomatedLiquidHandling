from ...Tools.Command.Command import Command
from .Options.PlacePlateOptions.PlacePlateOptions import PlacePlateOptions


class GetPlateCommand(Command):
    def __init__(self, OptionsInstance: PlacePlateOptions):
        Command.__init__(self)
        self.OptionsInstance: PlacePlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport ISwap"

    def GetCommandName(self) -> str:
        return "Place Plate"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
