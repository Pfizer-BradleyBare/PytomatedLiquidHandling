from ....Tools.Command.Command import Command
from .LoadTipsOptions import LoadTipsOptions


class LoadTipsCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: LoadTipsOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: LoadTipsOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Load Tips"

    def GetResponseKeys(self) -> list[str]:
        return ["GeneratedWasteSequence"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
