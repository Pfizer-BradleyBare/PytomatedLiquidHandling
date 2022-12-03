from ....Tools.Command.Command import Command
from .LoadTipsOptions import LoadTipsOptions


class InitializeCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: LoadTipsOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: LoadTipsOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Tip FTR"

    def GetCommandName(self) -> str:
        return "Initialize"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
