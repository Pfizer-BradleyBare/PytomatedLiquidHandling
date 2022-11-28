from ...Tools.Command.Command import Command
from .TerminateOptions import TerminateOptions


class TerminateCommand(Command):
    def __init__(self, Name: str, OptionsInstance: TerminateOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: TerminateOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Terminate"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
