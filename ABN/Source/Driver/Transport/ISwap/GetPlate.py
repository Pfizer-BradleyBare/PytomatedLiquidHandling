from ...Tools.Command.Command import Command
from .Options.GetPlateOptions.GetPlateOptions import GetPlateOptions


class GetPlateCommand(Command):
    def __init__(self, OptionsInstance: GetPlateOptions):
        Command.__init__(self)
        self.OptionsInstance: GetPlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport ISwap"

    def GetCommandName(self) -> str:
        return "Get Plate"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
