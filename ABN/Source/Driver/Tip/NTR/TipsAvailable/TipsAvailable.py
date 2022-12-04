from ....Tools.Command.Command import Command
from .TipsAvailableOptions import TipsAvailableOptions


class InitializeCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: TipsAvailableOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: TipsAvailableOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetResponseKeys(self) -> list[str]:
        return ["TipPosition"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
