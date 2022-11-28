from ....Tools.Command.Command import Command
from .CloseSpecialOptions import CloseSpecialOptions


class CloseSpecialCommand(Command):
    def __init__(self, Name: str, OptionsInstance: CloseSpecialOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: CloseSpecialOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Close Special"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
