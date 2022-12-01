from ...Tools.Command.Command import Command
from .MoveToTrackNumberOptions import MoveToTrackNumberOptions


class MoveToTrackNumberCommand(Command):
    def __init__(self, Name: str, OptionsInstance: MoveToTrackNumberOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: MoveToTrackNumberOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Unload Carrier"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
