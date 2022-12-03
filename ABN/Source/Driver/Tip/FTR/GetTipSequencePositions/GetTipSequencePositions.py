from ....Tools.Command.Command import Command
from .GetTipSequencePositionsOptions import GetTipSequencePositionsOptions


class InitializeCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: GetTipSequencePositionsOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: GetTipSequencePositionsOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
