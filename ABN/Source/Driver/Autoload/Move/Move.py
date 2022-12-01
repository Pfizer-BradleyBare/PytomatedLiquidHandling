from ...Tools.Command.Command import Command
from .MoveOptions import MoveOptions


class MoveCommand(Command):
    def __init__(self, Name: str, OptionsInstance: MoveOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: MoveOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Unload Carrier"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
