from ....Tools.Command.Command import Command
from .CloseOptions import CloseOptions


class CloseCommand(Command):
    def __init__(self, Name: str, OptionsInstance: CloseOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: CloseOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Close"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
