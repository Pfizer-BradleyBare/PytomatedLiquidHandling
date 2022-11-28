from ....Tools.Command.Command import Command
from .OpenOptions import OpenOptions


class OpenCommand(Command):
    def __init__(self, Name: str, OptionsInstance: OpenOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: OpenOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Open"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
