from ...Tools.Command.Command import Command
from .MoveOptions import MoveOptions


class MoveCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: MoveOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: MoveOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Move"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
