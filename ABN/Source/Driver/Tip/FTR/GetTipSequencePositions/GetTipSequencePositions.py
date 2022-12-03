from ....Tools.Command.Command import Command
from .GetTipSequencePositionsOptions import GetTipSequencePositionsOptions


class InitializeCommand(Command):
    def __init__(self, Name: str, OptionsInstance: GetTipSequencePositionsOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: GetTipSequencePositionsOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
