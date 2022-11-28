from ....Tools.Command.Command import Command
from .DeinitializeOptions import DeinitializeOptions


class DeinitializeCommand(Command):
    def __init__(self, Name: str, OptionsInstance: DeinitializeOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: DeinitializeOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Tip NTR"

    def GetCommandName(self) -> str:
        return "Deinitialize"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
